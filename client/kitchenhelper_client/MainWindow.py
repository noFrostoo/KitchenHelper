import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
  QMainWindow,
  QMessageBox
)
from PyQt5.QtCore import QEvent
from kitchenhelper_client.States.Idle import Idle

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("kitchenhelper_client/ui/MainWindow.ui", self)
        self.connectSignalsSlots()
        self.state = Idle(self)

    def connectSignalsSlots(self):
        pass
    
    def changeState():
        pass

    def keyPressEvent(self, e):
        self.state.keyPressEvent(e)

    def test(self):
        print("test")

    def about(self):
        QMessageBox.about(
            self,
            "About Kitchen Helper",
            "<p>Kitchen helper client app</p>"
        )
