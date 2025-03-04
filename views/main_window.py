from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLineEdit,
    QLabel, QPushButton, QGridLayout, QScrollArea,
    QMenuBar, QMenu, QAction, QDialog, QSpinBox,
    QHBoxLayout
)
from PyQt5.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from controllers.app_controller import AppController

class PreferencesDialog(QDialog):
    def __init__(self, controller: 'AppController', parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Préférences")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Taille de police
        font_layout = QHBoxLayout()
        font_label = QLabel("Taille de police:")
        self.font_spinbox = QSpinBox()
        self.font_spinbox.setRange(8, 24)
        self.font_spinbox.setValue(self.controller.model.get_font_size())
        self.font_spinbox.valueChanged.connect(self.update_font_size)
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_spinbox)
        layout.addLayout(font_layout)

        self.setLayout(layout)

    def update_font_size(self, size: int):
        self.controller.model.set_font_size(size)
        self.controller.update_theme()

class MainWindow(QMainWindow):
    def __init__(self, controller: 'AppController'):
        super().__init__()
        self.controller = controller
        self._setup_window_size()
        self.setWindowTitle("Mathopedia")
        self._setup_menu()
        self._setup_ui()

    def _setup_menu(self):
        """Configure la barre de menu"""
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu("Fichier")
        preferences_action = QAction("Préférences", self)
        preferences_action.triggered.connect(self.show_preferences)
        file_menu.addAction(preferences_action)
        
        # Menu Aide
        help_menu = menubar.addMenu("Aide")
        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_preferences(self):
        """Affiche la boîte de dialogue des préférences"""
        dialog = PreferencesDialog(self.controller, self)
        dialog.exec_()

    def show_about(self):
        """Affiche la boîte de dialogue À propos"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.about(self, "À propos de Mathopedia",
            "Mathopedia est une application de référence pour les formules mathématiques.\n\n"
            "Version 1.0\n"
            "© 2024 Mathopedia"
        )

    def _setup_window_size(self):
        """Configure la taille de la fenêtre selon les préférences"""
        window_size = self.controller.model.get_window_size()
        self.setGeometry(100, 100, window_size["width"], window_size["height"])

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Barre de recherche
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Recherchez une formule...")
        self.search_bar.textChanged.connect(self.search_formulas)
        layout.addWidget(self.search_bar, alignment=Qt.AlignCenter)

        # Bouton de changement de thème
        self.theme_button = QPushButton("Changer de thème")
        self.theme_button.clicked.connect(self.controller.toggle_theme)
        layout.addWidget(self.theme_button, alignment=Qt.AlignRight)

        # Zone de défilement pour les cartes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(900)

        cards_widget = QWidget()
        self.grid_layout = QGridLayout(cards_widget)

        # Création des cartes pour chaque discipline
        disciplines = self.controller.get_disciplines()
        for i, (domaine, description) in enumerate(disciplines.items()):
            card = self.create_card(domaine, description)
            self.grid_layout.addWidget(card, i // 3, i % 3)

        scroll_area.setWidget(cards_widget)
        layout.addWidget(scroll_area)

        central_widget.setLayout(layout)

    def create_card(self, domaine: str, description: str) -> QWidget:
        card = QWidget()
        card_layout = QVBoxLayout()

        label = QLabel(domaine)
        label.setStyleSheet(f"font-size: {self.controller.model.get_font_size() + 4}px; font-weight: bold;")

        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"font-size: {self.controller.model.get_font_size() + 8}px;")

        button = QPushButton("Voir les sous-catégories")
        button.clicked.connect(lambda: self.controller.open_subcategory_window(domaine))

        card_layout.addWidget(label)
        card_layout.addWidget(desc_label)
        card_layout.addWidget(button)
        card.setLayout(card_layout)

        return card

    def search_formulas(self, text: str):
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setVisible(True)
            
        if not text:
            return
            
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            domaine = widget.findChild(QLabel).text().lower()
            if text.lower() not in domaine:
                widget.setVisible(False)

    def apply_theme(self, styles: dict):
        """Applique le thème à la fenêtre principale"""
        font_size = self.controller.model.get_font_size()
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {styles['background']};
            }}
            QLabel {{
                color: {styles['text']};
                font-size: {font_size}px;
            }}
            QPushButton {{
                background-color: {styles['button_bg']};
                color: {styles['button_text']};
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-size: {font_size}px;
            }}
            QLineEdit {{
                background-color: {styles['input_bg']};
                color: {styles['input_text']};
                border: 1px solid {styles['card_border']};
                border-radius: 20px;
                padding: 10px;
                font-size: {font_size}px;
            }}
            QWidget {{
                background-color: {styles['background']};
            }}
            QMenuBar {{
                background-color: {styles['background']};
                color: {styles['text']};
            }}
            QMenuBar::item {{
                background-color: {styles['background']};
                color: {styles['text']};
            }}
            QMenuBar::item:selected {{
                background-color: {styles['button_bg']};
                color: {styles['button_text']};
            }}
            QMenu {{
                background-color: {styles['background']};
                color: {styles['text']};
            }}
            QMenu::item:selected {{
                background-color: {styles['button_bg']};
                color: {styles['button_text']};
            }}
        """)

    def resizeEvent(self, event):
        """Sauvegarde la taille de la fenêtre lors du redimensionnement"""
        super().resizeEvent(event)
        self.controller.model.set_window_size(self.width(), self.height()) 