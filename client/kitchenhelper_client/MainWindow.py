import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
  QMainWindow,
  QMessageBox
)
from PyQt5.QtCore import QEvent
from kitchenhelper_client.States.Idle import Idle
from kitchenhelper_client.VoiceCommandInterpreter import VoiceCommandInterpreter
from kitchenhelper_client.DataStore import DataStore
from kitchenhelper_client.Timers import Timers
from kitchenhelper_client.TextSpeaker import TextSpeaker

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # loading ui from .ui file
        loadUi("kitchenhelper_client/ui/MainWindow.ui", self)
        self.setUpObjects()
        self.connectSignalsSlots()
        self.state = Idle(self)
        self.mainArea.setCurrentIndex(1)
        self.showInfoScreen()

    def setUpObjects(self):
        """
        Main window works as a frame for grabing objets by states/objects
        """
        self.dataStore = DataStore()
        self.voiceCommandInterpreter = VoiceCommandInterpreter()
        self.timers = Timers(self)
        self.textSpeaker = TextSpeaker(self)

    def connectSignalsSlots(self):
        """
        functions to connect signals and slots
        """
        pass
    
    def showInfoScreen(self):
        self.TextArea.setText('<h1> Welcome to Kitchen Helper</h1>'
                               '<p> You can makes notes, set timers and look for recpies </p>'
                               '<p> You can look around the program by using keyboar or voice commands </p>'
                               '<p> KeyBoard actions depend on contex</p>'
                               '<p> Keyboard usage in idle state; 2 - change server, 4 - look up notes, 5 - voice command, 6 - find a recpie, 8 - see timers</p>'
                               '<p> Available voice commands: </p>'
                                    '<p style="text-indent:40px;">* Add a Note</p>'
                                    '<p style="text-indent:40px;">* Remove a Note</p>'
                                    '<p style="text-indent:40px;">* Show notes</p>'
                                    '<p style="text-indent:40px;">* Show note'
                                    '<p style="text-indent:40px;">* Show Timers</p>'
                                    '<p style="text-indent:40px;">* Show recipes</p>'
                                    '<p style="text-indent:40px;">* Get a Recipe</p>'
                                    '<p style="text-indent:40px;">* nothing</p>'
                                    '<p style="text-indent:40px;">* Add a timer</p>'
                                    '<p style="text-indent:40px;">* Pause timer</p>'
                                    '<p style="text-indent:40px;">* Stop timer</p>'
                                    '<p style="text-indent:40px;">* Select timer</p>'
                                    '<p style="text-indent:40px;">* Start a timer</p>')

    def changeState(self, newState):
        self.state.leave()
        self.state = newState(self)
        self.state.enter()

    def keyPressEvent(self, e):
        # we forward key event to a state and then to super object
        self.state.keyPressEvent(e)
        super().keyPressEvent(e)

    def about(self):
        QMessageBox.about(
            self,
            "About Kitchen Helper",
            "<p>Kitchen helper client app</p>"
        )

    def closeEvent(self, e):
        self.dataStore.save()
        self.textSpeaker.finish()
