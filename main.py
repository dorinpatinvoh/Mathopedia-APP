import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QGridLayout, QScrollArea
from PyQt5.QtCore import Qt

# Fonction pour charger les données depuis un fichier JSON
def load_json_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{filepath}' est introuvable.")
        return {}

# Fenêtre des sous-catégories
class SubCategoryWindow(QMainWindow):
    def __init__(self, discipline, subcategory_data):
        super().__init__()
        self.setWindowTitle(f"Sous-catégories de {discipline}")
        self.setGeometry(150, 150, 600, 400)

        layout = QVBoxLayout()

        # Ajouter une étiquette pour la discipline
        layout.addWidget(QLabel(f"Sous-catégories pour {discipline}"))

        # Création d'une zone de défilement pour afficher les cartes des sous-catégories
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(1000)

        cards_widget = QWidget()
        cards_layout = QGridLayout(cards_widget)

        # Vérifiez si la sous-catégorie existe dans les données JSON
        if discipline in subcategory_data:
            for i, (subcat, details) in enumerate(subcategory_data[discipline].items()):
                card = self.create_subcategory_card(subcat, details)
                cards_layout.addWidget(card, i // 3, i % 3)

        scroll_area.setWidget(cards_widget)
        layout.addWidget(scroll_area)

        # Créer un bouton pour revenir à l'interface principale
        back_button = QPushButton("Retour")
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def create_subcategory_card(self, subcat, details):
        card = QWidget()
        card_layout = QVBoxLayout()

        # Label pour la sous-catégorie
        label = QLabel(subcat)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")

        # Label pour la définition
        definition_label = QLabel(f"Définition : {details['definition']}")
        definition_label.setWordWrap(True)

        # Ajouter un bouton pour afficher les formules
        button = QPushButton("Voir les formules")
        button.clicked.connect(lambda: self.show_formulas(details['formulas']))

        card_layout.addWidget(label)
        card_layout.addWidget(definition_label)
        card_layout.addWidget(button)
        card.setLayout(card_layout)

        # Style de la carte
        card.setStyleSheet("""
            background-color: lightgrey; 
            border-radius: 10px; 
            padding: 10px; 
            margin: 10px; 
            width: 250px; 
            height: 150px;
        """)

        return card

    def show_formulas(self, formulas):
        formulas_window = QWidget()
        formulas_layout = QVBoxLayout(formulas_window)

        for formula in formulas:
            formulas_layout.addWidget(QLabel(f"Formule : {formula['name']}"))
            formulas_layout.addWidget(QLabel(f"Expression : {formula['formula']}"))
            formulas_layout.addWidget(QLabel(f"Exemple : {formula['example']}"))
            formulas_layout.addWidget(QLabel("--------------------"))  # Separator

        formulas_window.setWindowTitle("Formules")
        formulas_window.setGeometry(200, 200, 400, 300)
        formulas_window.setLayout(formulas_layout)
        formulas_window.show()

# Fenêtre principale de l'application
class MainWindow(QMainWindow):
    def __init__(self, disciplines, subcategories):
        super().__init__()

        self.setWindowTitle("Application Mathématique")
        self.setGeometry(100, 100, 800, 600)

        self.subcategories_data = subcategories

        # Création du widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Création de la mise en page
        layout = QVBoxLayout()

        # Barre de recherche
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Recherchez une formule...")
        self.search_bar.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 20px;
                background-color: #f9f9f9;
            }
        """)
        layout.addWidget(self.search_bar, alignment=Qt.AlignCenter)

        # Création d'une zone de défilement pour afficher les cartes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(900)

        cards_widget = QWidget()
        self.grid_layout = QGridLayout(cards_widget)

        # Création des cartes pour chaque discipline
        for i, (domaine, description) in enumerate(disciplines.items()):
            card = self.create_card(domaine, description)
            self.grid_layout.addWidget(card, i // 3, i % 3)

        scroll_area.setWidget(cards_widget)
        layout.addWidget(scroll_area)

        central_widget.setLayout(layout)

    def create_card(self, domaine, description):
        card = QWidget()
        card_layout = QVBoxLayout()

        # Label pour le domaine
        label = QLabel(domaine)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")

        # Label pour la description
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-size: 20px;")

        # Bouton pour afficher les sous-catégories
        button = QPushButton("Voir les sous-catégories")
        button.clicked.connect(lambda: self.open_subcategory_window(domaine))

        card_layout.addWidget(label)
        card_layout.addWidget(desc_label)
        card_layout.addWidget(button)
        card.setLayout(card_layout)

        # Style de la carte
        card.setStyleSheet("""
            background-color: grey; 
            border-radius: 10px; 
            padding: 10px; 
            margin: 10px; 
            width: 250px; 
            height: 150px;
        """)

        return card

    def open_subcategory_window(self, discipline):
        # Vérifie si la discipline a des sous-catégories
        if discipline in self.subcategories_data:
            self.subcategory_window = SubCategoryWindow(discipline, self.subcategories_data)
            self.subcategory_window.show()
        else:
            print(f"Pas de sous-catégories trouvées pour {discipline}")

# Fonction pour charger les données
def load_data():
    disciplines = load_json_file('data/disciplines.json')
    subcategories = load_json_file('data/subcategories.json')
    return disciplines, subcategories

# Point d'entrée de l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Chargement des données
    disciplines, subcategories = load_data()

    # Lancement de l'application principale
    window = MainWindow(disciplines, subcategories)
    window.show()

    sys.exit(app.exec_())
