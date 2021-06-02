# voiceCommands = [
    # "Add a Note", 
    # "Remove a Note",
    # "Show notes",
    # "Show note",
    # "Show Timers",
    # "Get a Recipe",
    # "Remove a Note",
    # "Add a timer",
    # "Pause timer",
    # "Stop timer",
    # "Select timer"
# ]
import enum

class VoiceCommands(enum.Enum):
    Add_A_Note = "Add a Note"
    Remove_a_Note = "Remove a Note"
    Show_notes = "Show notes"
    Show_note = "Show note"
    Show_Timers = "Show Timers"
    Get_a_Recipe = "Get a Recipe"
    Add_a_timer = "Add a timer"
    Pause_timer = "Pause timer"
    Stop_timer = "Stop timer"
    Select_Timer = "Select timer"
    Nothing = "nothing"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


