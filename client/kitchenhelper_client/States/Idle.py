from kitchenhelper_client.States.BaseState import BaseState
from kitchenhelper_client.States.Notes import Notes
from kitchenhelper_client.States.Timers import Timers
from kitchenhelper_client.States.VoiceCommand import VoiceCommand
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
  QMessageBox
)

class Idle(BaseState):
    def __init__(self, window):
        super().__init__(window)
        self.window.showInfoScreen()
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_2:
            self.window.test()
        elif e.key() == Qt.Key_4:
            self.stateToNotes()
        elif e.key() == Qt.Key_5:
            self.window.changeState(VoiceCommand)
        elif e.key() == Qt.Key_6:
            self.window.test() 
        elif e.key() == Qt.Key_8:
            self.window.changeState(Timers)
        elif e.key() == Qt.Key_Escape:
            self.window.close()
        else:
            QMessageBox.critical(
            self.window,
            "Error",
            "<p>Wrong key</p>"
            )

    def stateToNotes(self):
        self.window.changeState(Notes)
