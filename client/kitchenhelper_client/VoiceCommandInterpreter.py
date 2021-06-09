import difflib
from kitchenhelper_client.VoiceCommands import VoiceCommands

class VoiceCommandInterpreter:
    def __init__(self):
        self.commands = VoiceCommands.list()

    def understandCommand(self, text):
        # we match text againg comments and the one simmilar is the one that we take as a command
        command = difflib.get_close_matches(text, self.commands, n=1)
        if len(command) == 0:
            raise CouldNotUnderstandCommand
        return VoiceCommands(command[0])

class CouldNotUnderstandCommand(Exception):
    pass