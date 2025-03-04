import json
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Preferences:
    def __init__(self):
        self.preferences_file = "data/preferences.json"
        self.default_preferences = {
            "theme": "light",
            "window_size": {
                "width": 800,
                "height": 600
            },
            "font_size": 12
        }
        self.preferences = self.load_preferences()

    def load_preferences(self) -> Dict[str, Any]:
        """Charge les préférences depuis le fichier JSON"""
        try:
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r', encoding='utf-8') as f:
                    preferences = json.load(f)
                    logger.info("Préférences chargées avec succès")
                    return preferences
            else:
                logger.info("Aucun fichier de préférences trouvé, utilisation des préférences par défaut")
                return self.default_preferences.copy()
        except Exception as e:
            logger.error(f"Erreur lors du chargement des préférences : {str(e)}")
            return self.default_preferences.copy()

    def save_preferences(self) -> None:
        """Sauvegarde les préférences dans le fichier JSON"""
        try:
            os.makedirs(os.path.dirname(self.preferences_file), exist_ok=True)
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, indent=4)
            logger.info("Préférences sauvegardées avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde des préférences : {str(e)}")

    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une préférence par sa clé"""
        return self.preferences.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Définit une préférence et sauvegarde les changements"""
        self.preferences[key] = value
        self.save_preferences() 