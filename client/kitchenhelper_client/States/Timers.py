from kitchenhelper_client import States 
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
  QMessageBox
)

class Timers(States.BaseState.BaseState):
    def __init__(self, window):
        self.window = window
        if(self.window.timers.count() == 0):
            self.showInfo()
        else:
            self.showTimers()
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_0:
            self.addToId(0)
        elif e.key() == Qt.Key_1:
            self.addToId(1)
        elif e.key() == Qt.Key_2:
            self.addToId(2)
        elif e.key() == Qt.Key_3:
            self.addToId(3)
        elif e.key() == Qt.Key_4:
            self.addToId(4)
        elif e.key() == Qt.Key_5:
            self.addToId(5)
        elif e.key() == Qt.Key_6:
            self.addToId(6)
        elif e.key() == Qt.Key_7:
            self.addToId(7)
        elif e.key() == Qt.Key_8:
            self.addToId(8)
        elif e.key() == Qt.Key_9:
            self.addToId(9)
        elif e.key() == Qt.Key_Enter:
            self.showNote(self.id)
        elif e.key() == Qt.Key_Escape:
            self.window.changeState(States.Idle.Idle)
            self.window.List.clear()
        else:
            QMessageBox.critical(
            self.window,
            "Error",
            "<p>Wrong key</p>"
            )
    
    def showInfo(self):
        self.window.TextArea.setText('<h1> Welcome to Stopwatches Page</h1>'
                                '<p> You see this info because you have no Stopwatches</p>'
                                '<p> You can add Stopwatche by pressing + key</p>'
                                '<p> You can remove Stopwatche by pressing - and then entering Stopwatche number </p>'
                                '<p> You can look at pause/start by entering id and then pressing enter </p>'
                                '<p> You can go back by pressing escape key</p>'
                                '<p> Available voice commands: </p>')
    
    def showTimers(self):
        pass