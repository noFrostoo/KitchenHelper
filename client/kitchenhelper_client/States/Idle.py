from kitchenhelper_client.States.BaseState import BaseState
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
  QMessageBox
)

class Idle(BaseState):
    def __init__(self, window):
        super().__init__(window)
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_0:
            self.window.test()
        elif e.key() == Qt.Key_1:
            self.window.test()
        elif e.key() == Qt.Key_2:
            self.window.test()
        elif e.key() == Qt.Key_3:
            self.window.test()
        elif e.key() == Qt.Key_4:
            self.window.test()
        elif e.key() == Qt.Key_5:
            self.window.test()
        elif e.key() == Qt.Key_6:
            self.window.test()
        elif e.key() == Qt.Key_6:
            self.window.test()
        elif e.key() == Qt.Key_7:
            self.window.test()
        elif e.key() == Qt.Key_8:
            self.window.test()
        elif e.key() == Qt.Key_9:
            self.window.test()
        elif e.key() == Qt.Key_Escape:
            self.window.close()
        else:
            QMessageBox.about(
            self.window,
            "Error",
            "<p>Wrong key</p>"
            )
