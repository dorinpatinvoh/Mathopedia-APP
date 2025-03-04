import unittest
import json
import os
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
import sys

# Assurez-vous que le répertoire parent est dans le PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import MainWindow, SubCategoryWindow, load_json_file

class TestMathopedia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Créer une instance de QApplication pour les tests
        cls.app = QApplication(sys.argv)
        
        # Données de test
        cls.test_disciplines = {
            "Algèbre": "Description de l'algèbre",
            "Géométrie": "Description de la géométrie"
        }
        
        cls.test_subcategories = {
            "Algèbre": {
                "Équations": {
                    "definition": "Définition des équations",
                    "formulas": [
                        {
                            "name": "Équation du premier degré",
                            "formula": "ax + b = 0",
                            "example": "2x + 3 = 0"
                        }
                    ]
                }
            }
        }

    def test_load_json_file(self):
        # Test avec un fichier inexistant
        result = load_json_file('fichier_inexistant.json')
        self.assertEqual(result, {})

        # Test avec un fichier valide
        with open('test_data.json', 'w') as f:
            json.dump({"test": "data"}, f)
        result = load_json_file('test_data.json')
        self.assertEqual(result, {"test": "data"})
        os.remove('test_data.json')

    def test_main_window_creation(self):
        window = MainWindow(self.test_disciplines, self.test_subcategories)
        self.assertEqual(window.windowTitle(), "Mathopedia")
        self.assertTrue(hasattr(window, 'search_bar'))

    def test_search_functionality(self):
        window = MainWindow(self.test_disciplines, self.test_subcategories)
        # Test avec une recherche vide
        window.search_formulas("")
        # Test avec une recherche valide
        window.search_formulas("algèbre")

    def test_subcategory_window(self):
        window = SubCategoryWindow("Algèbre", self.test_subcategories)
        self.assertEqual(window.windowTitle(), "Sous-catégories de Algèbre")

if __name__ == '__main__':
    unittest.main() 