import difflib
from kitchenhelper_client.VoiceCommands import VoiceCommands
from PyQt5.QtWidgets import (
  QMessageBox
)
class VoiceCommandInterpreter:
    """
    Commands:

    """
    def __init__(self, voiceCommandHandler):
        self.voiceCommandHandler = voiceCommandHandler
        self.commands = VoiceCommands.list()

    def understandCommand(self, text):
        command = difflib.get_close_matches(text, self.commands, n=1)
        if len(command) == 0:
            raise CouldNotUnderstandCommand
        return VoiceCommands(command[0])

class CouldNotUnderstandCommand(Exception):
    pass