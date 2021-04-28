class DataStore:
    def __init__(self, window):
        self.window = window
        self.notes = {
            1 : {
            'noteId': 1,
            'title': 'note1',
            'note': 'notenote'
            },
            2 : {
            'noteId': 2,
            'title': 'note2',
            'note': 'notenote'
            },
            3 : {
            'noteId': 3,
            'title': 'note3',
            'note': 'notenote'
            },
            4 : {
            'noteId': 4,
            'title': 'note4',
            'note': 'notenote'
            },
        }
    
    def getNotesList(self):
        notesList = []
        for note in self.notes.values():
            notesList.append({
                'noteId': note['noteId'],
                'title': note['title']
            })
        return notesList
    

    def getNote(self, id):
        return self.notes[id]
