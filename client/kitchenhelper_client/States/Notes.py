# from kitchenhelper_client.States.BaseState import BaseState
# from kitchenhelper_client.States.Idle import Idle
from kitchenhelper_client import States 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
  QMessageBox
)

class Notes(States.BaseState.BaseState):
    def __init__(self, window):
        super().__init__(window)
        self.showInfo()
        self.showNotesInfo()
        self.id = 0
        self.idSize = 0

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
        self.window.TextArea.setText('<h1> Welcome to Notes Page</h1>'
                                '<p> You can makes note by pressing + key</p>'
                                '<p> You can remove note by pressing - and then entering note number </p>'
                                '<p> You can look at note by entering id and then pressing enter </p>'
                                '<p> You can go back by pressing escape key</p>'
                                '<p> Available voice commands: </p>')
    
    def showNotesInfo(self):
        self.list = self.window.dataStore.getNotesList()
        for note in self.list:
            self.window.List.addItem(f'Id: {note["noteId"]}, {note["title"]}')
    
    def addToId(self, number):
        self.id += self.idSize * 10 + number
        self.idSize += 1


    def showNote(self, id):
        note = self.window.dataStore.getNote(id)
        self.window.TextArea.setText(f'<h1>{note["title"]}</h1>'
                                     f'{note["note"]}')
        self.id = 0
        self.idSize = 0