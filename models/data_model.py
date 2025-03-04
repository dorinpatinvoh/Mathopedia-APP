from typing import Dict, List, Optional, Any, Tuple
import json
import logging
from .preferences import Preferences

logger = logging.getLogger(__name__)

class DataModel:
    def __init__(self):
        self.disciplines: Dict[str, str] = {}
        self.subcategories: Dict[str, Dict[str, Any]] = {}
        self.preferences = Preferences()
        self.load_data()

    def load_data(self) -> None:
        """Charge les données depuis les fichiers JSON"""
        self.disciplines = self._load_json_file('data/disciplines.json')
        self.subcategories = self._load_json_file('data/subcategories.json')

    def _load_json_file(self, filepath: str) -> Dict[str, Any]:
        """Charge et parse un fichier JSON"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.info(f"Fichier {filepath} chargé avec succès")
                return data
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du fichier {filepath}: {str(e)}")
            return {}

    def get_disciplines(self) -> Dict[str, str]:
        """Retourne toutes les disciplines"""
        return self.disciplines

    def get_subcategories(self, discipline: str) -> Dict[str, Any]:
        """Retourne les sous-catégories d'une discipline"""
        return self.subcategories.get(discipline, {})

    def get_formulas(self, discipline: str, subcategory: str) -> List[Dict[str, str]]:
        """Retourne les formules d'une sous-catégorie"""
        if discipline in self.subcategories and subcategory in self.subcategories[discipline]:
            return self.subcategories[discipline][subcategory].get('formulas', [])
        return []

    def set_theme(self, theme: str) -> None:
        """Change le thème de l'application"""
        if theme in ["light", "dark"]:
            self.preferences.set("theme", theme)
            logger.info(f"Thème changé pour {theme}")

    def get_theme(self) -> str:
        """Retourne le thème actuel"""
        return self.preferences.get("theme", "light")

    def get_theme_styles(self) -> Dict[str, str]:
        """Retourne les styles CSS en fonction du thème"""
        if self.get_theme() == "dark":
            return {
                "background": "#2b2b2b",
                "text": "#ffffff",
                "card_bg": "#3b3b3b",
                "card_border": "#4b4b4b",
                "button_bg": "#4b4b4b",
                "button_text": "#ffffff",
                "input_bg": "#3b3b3b",
                "input_text": "#ffffff"
            }
        else:
            return {
                "background": "#ffffff",
                "text": "#000000",
                "card_bg": "#f0f0f0",
                "card_border": "#dddddd",
                "button_bg": "#e0e0e0",
                "button_text": "#000000",
                "input_bg": "#f9f9f9",
                "input_text": "#000000"
            }

    def get_window_size(self) -> Dict[str, int]:
        """Retourne la taille de la fenêtre"""
        return self.preferences.get("window_size", {"width": 800, "height": 600})

    def set_window_size(self, width: int, height: int) -> None:
        """Définit la taille de la fenêtre"""
        self.preferences.set("window_size", {"width": width, "height": height})

    def get_font_size(self) -> int:
        """Retourne la taille de la police"""
        return self.preferences.get("font_size", 12)

    def set_font_size(self, size: int) -> None:
        """Définit la taille de la police"""
        self.preferences.set("font_size", size) 