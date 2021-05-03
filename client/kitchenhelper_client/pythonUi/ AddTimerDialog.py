from kitchenhelper_client.pythonUi.ListenDialog import ListenDialog
from PyQt5.QtWidgets import (
  QApplication
)
class AddNoteDialog(ListenDialog):
    def __init__(self, window):
        super().__init__(window)
        self.label.setText("Listening for title")
    
    def doTheListen(self):
        audio = self.vi.listen()
        self.label.setText("Analizing...")
        QApplication.processEvents()
        self.text = self.vi.recognize(audio)
        self.label.setText("Listening for note contents")
        QApplication.processEvents()
        audio = self.vi.listen()
        self.label.setText("Analizing...")
        QApplication.processEvents()
        self.note = self.vi.recognize(audio)

    def getNote(self):
        return self.note
    
    def getTitle(self):
        return self.text