from typing import Dict, Any, Optional
from models.data_model import DataModel
from views.main_window import MainWindow
from views.subcategory_window import SubCategoryWindow

class AppController:
    def __init__(self):
        self.model = DataModel()
        self.main_window: Optional[MainWindow] = None
        self.subcategory_window: Optional[SubCategoryWindow] = None

    def start(self):
        """Démarre l'application"""
        self.main_window = MainWindow(self)
        self.main_window.show()

    def get_disciplines(self) -> Dict[str, str]:
        """Récupère toutes les disciplines"""
        return self.model.get_disciplines()

    def get_subcategories(self, discipline: str) -> Dict[str, Any]:
        """Récupère les sous-catégories d'une discipline"""
        return self.model.get_subcategories(discipline)

    def get_formulas(self, discipline: str, subcategory: str) -> list:
        """Récupère les formules d'une sous-catégorie"""
        return self.model.get_formulas(discipline, subcategory)

    def open_subcategory_window(self, discipline: str):
        """Ouvre la fenêtre des sous-catégories"""
        if self.subcategory_window:
            self.subcategory_window.close()
        self.subcategory_window = SubCategoryWindow(self, discipline)
        self.subcategory_window.show()

    def toggle_theme(self):
        """Bascule entre le thème clair et sombre"""
        current_theme = self.model.get_theme()
        new_theme = "dark" if current_theme == "light" else "light"
        self.model.set_theme(new_theme)
        self.update_theme()

    def update_theme(self):
        """Met à jour le thème de toutes les fenêtres"""
        styles = self.model.get_theme_styles()
        if self.main_window:
            self.main_window.apply_theme(styles)
        if self.subcategory_window:
            self.subcategory_window.apply_theme(styles) 