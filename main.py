import sys
import logging
from PyQt5.QtWidgets import QApplication
from controllers.app_controller import AppController

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mathopedia.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Point d'entrée de l'application"""
    try:
        app = QApplication(sys.argv)
        controller = AppController()
        controller.start()
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f"Erreur lors du démarrage de l'application : {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
