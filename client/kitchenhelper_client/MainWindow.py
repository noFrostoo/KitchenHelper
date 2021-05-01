import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
  QMainWindow,
  QMessageBox
)
from PyQt5.QtCore import QEvent
from kitchenhelper_client.States.Idle import Idle
from kitchenhelper_client.Config import Config
from kitchenhelper_client.RequestHandler import RequestHandler
from kitchenhelper_client.VoiceCommandHandler import VoiceCommandHandler
from kitchenhelper_client.VoiceCommandInterpreter import VoiceCommandInterpreter
from kitchenhelper_client.DataStore import DataStore
from kitchenhelper_client.Timers import Timers

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("kitchenhelper_client/ui/MainWindow.ui", self)
        self.setUpObjects()
        self.connectSignalsSlots()
        self.state = Idle(self)
        self.mainArea.setCurrentIndex(1)
        self.showInfoScreen()

    def setUpObjects(self):
        self.config = Config()
        self.dataStore = DataStore(self)
        self.requestHandler = RequestHandler(self.config)
        self.voiceCommandHandler = VoiceCommandHandler()
        self.voiceCommandInterpreter = VoiceCommandInterpreter(self.voiceCommandHandler)
        self.timers = Timers(self)

    def setUpPointersToUiElements(self):
        pass

    def connectSignalsSlots(self):
        pass
    
    def showInfoScreen(self):
        self.TextArea.setText('<h1> Welcome to Kitchen Helper</h1>'
                               '<p> You can makes notes, set timers and look for recpies </p>'
                               '<p> You can look around the program by using keyboar or voice commands </p>'
                               '<p> KeyBoard actions depend on contex</p>'
                               '<p> Keyboard usage in idle state; 2 - change server, 4 - look up notes, 5 - voice command, 6 - find a recpie, 8 - see timers</p>'
                               '<p> Available voice commands: </p>')

    def changeState(self, newState):
        self.state = newState(self)

    def keyPressEvent(self, e):
        self.state.keyPressEvent(e)

    def test(self):
        print("test")

    def about(self):
        QMessageBox.about(
            self,
            "About Kitchen Helper",
            "<p>Kitchen helper client app</p>"
        )
