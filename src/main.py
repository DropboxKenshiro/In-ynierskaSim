import sys
import logging
from datetime import datetime
from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow

if __name__ == '__main__':
    logging.basicConfig(filename=f"qsimlog-{datetime.now().isoformat().replace(':', '')}.txt", encoding="utf-8", level=logging.INFO)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
