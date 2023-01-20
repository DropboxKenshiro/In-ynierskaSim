from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMainWindow, QWidget

from ui.mainwindow_ui import Ui_MainWindow
from simulationwindows import TeleportationWindow, DeutschJozsaWindow, SimpleEntaglementWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.teleportationButton.released.connect(self.run_teleportation)
        self.ui.deutsch_button.released.connect(self.run_deutsch)
        self.ui.simple_button.released.connect(self.run_simple)

        self.ui.wat_logo.setPixmap(QPixmap("res/Logo_WAT_transparent.png"))

        self.child_window = None

    @Slot()
    def run_teleportation(self):
        if self.child_window is QWidget:
            self.child_window.close()
        self.child_window = TeleportationWindow()
        self.child_window.show()

    @Slot()
    def run_deutsch(self):
        if self.child_window is QWidget:
            self.child_window.close()
        self.child_window = DeutschJozsaWindow()
        self.child_window.show()

    @Slot()
    def run_simple(self):
        if self.child_window is QWidget:
            self.child_window.close()
        self.child_window = SimpleEntaglementWindow()
        self.child_window.show()
