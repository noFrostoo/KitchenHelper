from kitchenhelper_client import States
from kitchenhelper_client.pythonUi.ListenDialog import ListenDialog 
from kitchenhelper_client.VoiceCommands import VoiceCommands
from kitchenhelper_client.VoiceCommandInterpreter import CouldNotUnderstandCommand
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
  QMessageBox
)

class VoiceCommand(States.BaseState.BaseState):
    def __init__(self, window):
        self.window = window

    def enter(self):
        self.window.statusbar.showMessage('Listening for commands')
        self.showListening()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.window.changeState(States.Idle.Idle)
    
    def showListening(self):
        dialog = ListenDialog(self.window)
        if dialog.exec():
            self.command = dialog.getText()
            print(f"text from speech recognition: {self.command}")
            self.execCommand()
        else:
            QMessageBox.critical(
            self.window,
            "Error",
            f"<p>{dialog.getError()}</p>"
            )
            self.window.changeState(States.Idle.Idle)
    
    def execCommand(self):
        try:
            self.command = self.window.voiceCommandInterpreter.understandCommand(self.command)
            print(f"after matching command: {self.command}")
        except CouldNotUnderstandCommand:
            return self.commandNotUnderstood()
        self.decideAction()

    def decideAction(self):
        if self.command == VoiceCommands.Add_A_Note:
            self.window.changeState(States.Notes.Notes)
            self.window.state.addNote()
        elif self.command == VoiceCommands.Remove_a_Note:
            self.window.changeState(States.Notes.Notes)
            self.window.state.removeNote()
        elif self.command == VoiceCommands.Show_notes:
            self.window.changeState(States.Notes.Notes)
        elif self.command == VoiceCommands.Show_note:
            self.window.changeState(States.Notes.Notes)
        elif self.command == VoiceCommands.Show_Timers:
            self.window.changeState(States.Timers.Timers)
        elif self.command == VoiceCommands.Show_recipes:
            self.window.changeState(States.Recipes.Recipes)
        elif self.command == VoiceCommands.Get_a_Recipe:
            self.window.changeState(States.Recipes.Recipes)
            self.window.state.listenToDish()
        elif self.command == VoiceCommands.Pause_timer:
            self.window.changeState(States.Timers.Timers)
            self.window.state.pauseTimer()
        elif self.command == VoiceCommands.Stop_timer:
            self.window.changeState(States.Timers.Timers)
            self.window.state.stopTimer()
        elif self.command == VoiceCommands.Start_Timer:
            self.window.changeState(States.Timers.Timers)
            self.window.state.startTimer()
        elif self.command == VoiceCommands.Select_Timer:
            self.window.changeState(States.Timers.Timers)
            self.window.state.selectTimerVoice()
            self.window.state.showSelectedTimer()
        
    def notImplemted(self):
        QMessageBox.critical(
        self.window,
        "Error",
        "<p>not implemented yed</p>"
        )
        self.window.changeState(States.Idle.Idle)
    
    def commandNotUnderstood(self):
        QMessageBox.critical(
        self.window,
        "Error",
        f"<p>couldn't understand command</p>"
        )
        self.window.changeState(States.Idle.Idle) 