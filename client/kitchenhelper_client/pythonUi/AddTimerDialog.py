from kitchenhelper_client.pythonUi.ListenDialog import ListenDialog
from PyQt5.QtWidgets import (
  QApplication,
)
from word2number import w2n
import speech_recognition as sr

class AddTimerDialog(ListenDialog):
    def __init__(self, window):
        super().__init__(window)
        self.label.setText("Listening for title")
    
    def doTheListen(self):
        audio = self.vi.listen()
        self.label.setText("Analyzing...")
        QApplication.processEvents()
        self.text = self.vi.recognize(audio)
        self.label.setText("Listening for minutes")
        QApplication.processEvents()
        audio = self.vi.listen()
        self.label.setText("Analyzing...")
        QApplication.processEvents()
        self.minutesText = self.vi.recognize(audio)
        self.label.setText("Listening for seconds")
        QApplication.processEvents()
        audio = self.vi.listen()
        self.label.setText("Analyzing...")
        QApplication.processEvents()
        self.secondsText = self.vi.recognize(audio)

    def process(self):
        self.minutes = w2n.word_to_num(self.minutesText)
        self.seconds = w2n.word_to_num(self.secondsText)
        self.ms = self.seconds*1000 + self.minutes*60000

    def listen(self):
        try:
            self.doTheListen()
            self.process()
            self.accept()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            self.error = "Google Speech Recognition could not understand audio"
            self.reject()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            self.error = "Could not request results from Google Speech Recognition service; {0}".format(e)
            self.reject()
        except ValueError as e:
            print("Could not understand the number")
            self.error = "Could not understand the number"
            self.reject()
            return

    def getTime(self):
        return self.ms
    
    def getTitle(self):
        return self.text