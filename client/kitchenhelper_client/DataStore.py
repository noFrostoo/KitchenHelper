class DataStore:
    def __init__(self, window):
        self.window = window
        self.nextId = 5
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

    def addNote(self, title, text):
        self.notes[self.nextId] = {
            'noteId': self.nextId,
            'title': title,
            'note': text
        }
        self.nextId += 1
    
    def removeNote(self, id):
        self.notes.pop(id, None)

    def editNote(self, id, text):
        self.notes[id]['note'] = text
