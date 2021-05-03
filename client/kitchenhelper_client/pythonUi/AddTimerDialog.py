from kitchenhelper_client.pythonUi.ListenDialog import ListenDialog
from PyQt5.QtWidgets import (
  QApplication
)
from word2number import w2n

class AddTimerDialog(ListenDialog):
    def __init__(self, window):
        super().__init__(window)
        self.label.setText("Listening for title")
    
    def doTheListen(self):
        audio = self.vi.listen()
        self.label.setText("Analizing...")
        QApplication.processEvents()
        self.text = self.vi.recognize(audio)
        self.label.setText("Listening for minutes")
        QApplication.processEvents()
        audio = self.vi.listen()
        self.label.setText("Analizing...")
        QApplication.processEvents()
        minutes = self.vi.recognize(audio)
        minutes = w2n.word_to_num(minutes)
        self.label.setText("Listening for seconds")
        QApplication.processEvents()
        audio = self.vi.listen()
        self.label.setText("Analizing...")
        QApplication.processEvents()
        seconds = self.vi.recognize(audio)
        seconds = w2n.word_to_num(seconds)
        self.ms = seconds*1000 + minutes*60000
        

    def getTime(self):
        return self.ms
    
    def getTitle(self):
        return self.text