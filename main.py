import sys
from PyQt5.QtWidgets import QApplication
from gui import GUI
from logger import get_logger

logger = get_logger(__name__, log_level="DEBUG")

if __name__ == "__main__":
    logger.debug("Application starting")
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    logger.debug("GUI window shown")
    sys.exit(app.exec_())
    logger.debug("Application exiting")
