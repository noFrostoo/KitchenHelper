import sys
from kitchenhelper_client.pythonUi.OneLabelDialog_ui import Ui_Dialog
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
import speech_recognition as sr
from PyQt5.QtWidgets import (
  QDialog
)

class ListenDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.connectSignalsSlots()
        self.error = 'nothing'
        self.text = 0
        QTimer.singleShot(160, self.listen) # value found with try and  error so has to repeated for rasbery pi

    # def showEvent(self, e):
    #     print('show')
    #     super().showEvent(e)
    #     self.listen()
    
    def connectSignalsSlots(self):
        pass
    
    @pyqtSlot()
    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Say something!")
            audio = r.listen(source)
        try:
            self.text = r.recognize_google(audio)
            print("Google Speech Recognition thinks you said " + self.text)
            self.accept()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            self.error = "Google Speech Recognition could not understand audio"
            self.reject()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            self.error = "Could not request results from Google Speech Recognition service; {0}".format(e)
            self.reject()
    
    def getText(self):
        return self.text
    
    def getError(self):
        return self.error