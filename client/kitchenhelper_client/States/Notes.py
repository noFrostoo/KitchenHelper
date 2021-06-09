# from kitchenhelper_client.States.BaseState import BaseState
# from kitchenhelper_client.States.Idle import Idle
from kitchenhelper_client import States 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
  QMessageBox
)
from kitchenhelper_client.pythonUi.AddNoteDialog import AddNoteDialog
from kitchenhelper_client.pythonUi.ListenDialog import ListenDialog 
from word2number import w2n

class Notes(States.BaseState.BaseState):
    def __init__(self, window):
        super().__init__(window)
        self.id = 0
        self.idSize = 0
        self.selectedNote = None
        self.seletedId = -1

    def enter(self):
        # when entering a state we make sure the index is set to one
        # text area is under index 0
        # we always update notes list and if there is selected note we show if
        # othewise we simply show info
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
        elif e.key() == Qt.Key_Plus:
            self.addNote()
        elif e.key() == Qt.Key_Minus:
            self.removeNote(self.id)
        elif e.key() == Qt.Key_Escape:
            self.window.changeState(States.Idle.Idle)
            self.window.List.clear()
        elif e.key() == Qt.Key_Comma:
            self.window.List.clear()
            self.window.changeState(States.VoiceCommand.VoiceCommand)
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
                                '<p>You can activate voice command by clicking comma(,)</p>')
    
    def showNotesInfo(self):
        for i, note in enumerate(self.window.dataStore.getAllNotes()):
            self.window.List.addItem(f'{i}: {note.title}')
    
    def addToId(self, number):
        self.id += self.idSize * 10 + number
        self.idSize += 1
        self.window.statusbar.showMessage(f'Note id: {self.id}')


    def selectNote(self, index):
        dictList = list(self.window.dataStore.getAllNotes())
        self.selectedNote = dictList[index]
        self.window.textSpeaker.say("Note Title is " + self.selectedNote.title)
        self.window.textSpeaker.say("Note contents are  " + self.selectedNote.content)
        self.seletedId = self.selectedNote.id
        self.id = 0
        self.idSize = 0
        self.showSelectedNote()
    
    def showSelectedNote(self):
        self.window.TextArea.setText(f'<h1>{self.selectedNote.title}</h1>'
                                f'{self.selectedNote.content}')
        self.window.statusbar.showMessage(f'Selected note: {self.selectedNote.title}')

    def removeNote(self):
        self.window.dataStore.removeNote(self.seletedId)
        QMessageBox.info(
            self.window,
            "INFO",
            f"<p>Note removed</p>"
        )
        self.showInfo()

    def addNote(self):
        addNoteDialog = AddNoteDialog(self.window)
        # if dialog was succesful we progres otherewise we show error message box
        if addNoteDialog.exec():
            newNoteTitle = addNoteDialog.getTitle()
            newNoteContents = addNoteDialog.getNote()
            self.seletedId =  self.window.dataStore.addNote(newNoteTitle, newNoteContents)
            for i, note in enumerate(self.window.dataStore.getAllNotes()):
                if note.id == self.seletedId:
                    self.seletedId = i
                    break
            self.selectNote(self.seletedId)
            self.updateNotesList()
        else:
            QMessageBox.critical(
            self.window,
            "Error",
            f"<p>{addNoteDialog.getError()}</p>"
            )
    
    def updateNotesList(self):
        self.window.List.clear()
        self.showNotesInfo()
    
    def selectNoteVoice(self):
        dialog = ListenDialog(self.window, 'Listing to note id...')
        if dialog.exec():
            NoteID = self.minutes = w2n.word_to_num(dialog.getText())
            self.selectNote(NoteID)
        else:
            QMessageBox.critical(
            self.window,
            "Error",
            f"<p>{dialog.getError()}, timer not selected</p>"
            )