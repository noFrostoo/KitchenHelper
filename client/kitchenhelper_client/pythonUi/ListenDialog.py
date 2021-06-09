import sys
from kitchenhelper_client.pythonUi.OneLabelDialog_ui import Ui_Dialog
from kitchenhelper_client.VoiceInterpreter import VoiceInterpreter
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
import speech_recognition as sr
from PyQt5.QtWidgets import (
  QDialog,
  QApplication
)

class ListenDialog(QDialog, Ui_Dialog):
    def __init__(self, window, labelText = 'Listening to voice command ...'):
        super().__init__(window)
        self.window = window
        self.setupUi(self)
        self.label.setText(labelText)
        self.connectSignalsSlots()
        self.error = 'nothing'
        self.text = 0
        self.vi = VoiceInterpreter()
        QTimer.singleShot(400, self.listen) # value found with try and  error so has to repeated for rasbery pi
        
    
    def connectSignalsSlots(self):
        pass

    def listen(self):
        """
        Does the listening if erros appeaed  rejecets the dialog
        """
        try:
            self.doTheListen()
            self.accept()
        except sr.UnknownValueError:
            self.error = "Google Speech Recognition could not understand audio"
            self.reject()
        except sr.RequestError as e:
            self.error = "Could not request results from Google Speech Recognition service; {0}".format(e)
            self.reject()
    
    def getText(self):
        return self.text
    
    def getError(self):
        return self.error
    
    def doTheListen(self):
        """
        Does the actual listening and if needed changes label on dialog
        """
        audio = self.vi.listen()
        self.label.setText('Analyzing...')
        QApplication.processEvents() # it is needed for qt to change label
        self.text = self.vi.recognize(audio)