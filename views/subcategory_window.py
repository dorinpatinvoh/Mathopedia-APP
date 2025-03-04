from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QGridLayout, QScrollArea
)
from PyQt5.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.app_controller import AppController

class SubCategoryWindow(QMainWindow):
    def __init__(self, controller: 'AppController', discipline: str):
        super().__init__()
        self.controller = controller
        self.discipline = discipline
        self.formulas_window = None  # Ajout de l'attribut pour stocker la fenêtre des formules
        self.setGeometry(150, 150, 600, 400)
        self.setWindowTitle(f"Sous-catégories de {discipline}")
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Label pour la discipline
        layout.addWidget(QLabel(f"Sous-catégories pour {self.discipline}"))

        # Zone de défilement pour les cartes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(1000)

        cards_widget = QWidget()
        cards_layout = QGridLayout(cards_widget)

        # Création des cartes pour chaque sous-catégorie
        subcategories = self.controller.get_subcategories(self.discipline)
        for i, (subcat, details) in enumerate(subcategories.items()):
            card = self.create_subcategory_card(subcat, details)
            cards_layout.addWidget(card, i // 3, i % 3)

        scroll_area.setWidget(cards_widget)
        layout.addWidget(scroll_area)

        # Bouton retour
        back_button = QPushButton("Retour")
        back_button.clicked.connect(self.close)
        layout.addWidget(back_button)

        central_widget.setLayout(layout)

    def create_subcategory_card(self, subcat: str, details: dict) -> QWidget:
        card = QWidget()
        card_layout = QVBoxLayout()

        # Label pour la sous-catégorie
        label = QLabel(subcat)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")

        # Label pour la définition
        definition_label = QLabel(f"Définition : {details['definition']}")
        definition_label.setWordWrap(True)

        # Bouton pour afficher les formules
        button = QPushButton("Voir les formules")
        button.clicked.connect(lambda: self.show_formulas(subcat))

        card_layout.addWidget(label)
        card_layout.addWidget(definition_label)
        card_layout.addWidget(button)
        card.setLayout(card_layout)

        return card

    def show_formulas(self, subcategory: str):
        # Fermer la fenêtre existante si elle existe
        if self.formulas_window:
            self.formulas_window.close()
            
        # Créer une nouvelle fenêtre
        self.formulas_window = QWidget()
        self.formulas_window.setWindowFlags(Qt.Window)  # Rendre la fenêtre indépendante
        formulas_layout = QVBoxLayout(self.formulas_window)

        # Ajouter un titre
        title_label = QLabel(f"Formules de {subcategory}")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        formulas_layout.addWidget(title_label)
        formulas_layout.addWidget(QLabel("--------------------"))

        # Afficher les formules
        formulas = self.controller.get_formulas(self.discipline, subcategory)
        for formula in formulas:
            formula_group = QWidget()
            formula_layout = QVBoxLayout(formula_group)
            
            name_label = QLabel(f"Formule : {formula['name']}")
            name_label.setStyleSheet("font-weight: bold;")
            formula_layout.addWidget(name_label)
            
            formula_layout.addWidget(QLabel(f"Expression : {formula['formula']}"))
            formula_layout.addWidget(QLabel(f"Exemple : {formula['example']}"))
            formula_layout.addWidget(QLabel("--------------------"))
            
            formulas_layout.addWidget(formula_group)

        # Ajouter un bouton de fermeture
        close_button = QPushButton("Fermer")
        close_button.clicked.connect(self.formulas_window.close)
        formulas_layout.addWidget(close_button)

        self.formulas_window.setWindowTitle(f"Formules - {subcategory}")
        self.formulas_window.setGeometry(200, 200, 600, 500)  # Fenêtre plus grande
        self.formulas_window.show()

    def apply_theme(self, styles: dict):
        """Applique le thème à la fenêtre des sous-catégories"""
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {styles['background']};
            }}
            QLabel {{
                color: {styles['text']};
            }}
            QPushButton {{
                background-color: {styles['button_bg']};
                color: {styles['button_text']};
                border: none;
                padding: 8px;
                border-radius: 4px;
            }}
            QWidget {{
                background-color: {styles['background']};
            }}
        """) 