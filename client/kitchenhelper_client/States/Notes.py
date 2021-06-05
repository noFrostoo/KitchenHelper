# from kitchenhelper_client.States.BaseState import BaseState
# from kitchenhelper_client.States.Idle import Idle
from kitchenhelper_client import States 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
  QMessageBox
)
from kitchenhelper_client.pythonUi.AddNoteDialog import AddNoteDialog

class Notes(States.BaseState.BaseState):
    def __init__(self, window):
        super().__init__(window)
        self.id = 0
        self.idSize = 0
        self.selectedNote = None
        # self.addNoteDialog = AddNoteDialog(window)

    def enter(self):
        self.window.mainArea.setCurrentIndex(1)
        self.updateNotesList()
        if self.selectedNote is not None:
            self.showSelectedNote()
        else:
            self.showInfo()

    def leave(self):
        self.window.List.clear()

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
            self.selectNote(self.id)
            self.showSelectedNote()
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
        for i, note in enumerate(self.window.dataStore.getAllNotes()):
            self.window.List.addItem(f'{i}: {note.title}')
    
    def addToId(self, number):
        self.id += self.idSize * 10 + number
        self.idSize += 1
        self.window.statusbar.showMessage(f'Note id: {self.id}')


    def selectNote(self, id):
        self.selectedNote = self.window.dataStore.getNote(id)
        self.window.textSpeaker.say("Note Title is " + self.selectedNote.title)
        self.window.textSpeaker.say("Note contents are  " + self.selectedNote.content)
        self.id = 0
        self.idSize = 0
    
    def showSelectedNote(self):
        self.window.TextArea.setText(f'<h1>{self.selectedNote.title}</h1>'
                                f'{self.selectedNote.content}')
        self.window.statusbar.showMessage(f'Selected note: {self.selectedNote.title}')

    def removeNote(self):
        pass

    def addNote(self):
        addNoteDialog = AddNoteDialog(self.window)
        if addNoteDialog.exec():
            newNoteTitle = addNoteDialog.getTitle()
            print(f"text from speech recognition: {newNoteTitle}")
            newNoteContents = addNoteDialog.getNote()
            self.window.dataStore.addNote(newNoteTitle, newNoteContents)
        else:
            QMessageBox.critical(
            self.window,
            "Error",
            f"<p>{addNoteDialog.getError()}</p>"
            )
    
    def updateNotesList(self):
        self.window.List.clear()
        self.showNotesInfo()