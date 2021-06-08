from hashlib import sha1
import json
from pathlib import Path
from urllib.request import urlretrieve

from PyQt5.QtWidgets import QMessageBox

from .pythonUi.ServerDialog import ServerDialog
from .RequestHandler import RequestHandler
from .schemas import Note, NoteBase, Recipe

class DataStore:
    DATASTORE_FILE = Path('data.json')
    IMAGE_DIR = Path('.kh_images')

    def __init__(self):
        self.data = {}

        if self.DATASTORE_FILE.exists():
            with self.DATASTORE_FILE.open() as fp:
                self.data = json.load(fp)

            self.data['notes'] = {int(k): Note.parse_obj(v) for k, v in self.data['notes'].items()}
            self.data['recipes'] = {k: Recipe.parse_obj(v) for k, v in self.data['recipes'].items()}
            
            self.req_handler = RequestHandler(self.data['server_address'], self.data['user_id'])

            self.data['notes'] = {note.id: note for note in self.req_handler.syncNotes(self.data['notes'].values())}
        
        else:
            self.data['server_address'] = self._get_server_address()
            self.data['notes'] = {}
            self.data['recipes'] = {}
            self.req_handler = RequestHandler(self.data['server_address'], None)
            self.data['user_id'] = self.req_handler.registerUser()

        self.save()

    def save(self):
        to_save = self.data.copy()
        to_save['notes'] = {k: v.dict() for k, v in self.data['notes'].items()}
        to_save['recipes'] = {k: v.dict() for k, v in self.data['recipes'].items()}

        with self.DATASTORE_FILE.open('w') as fp:
            json.dump(to_save, fp)


    @staticmethod
    def _get_server_address():
        dialog = ServerDialog()

        if dialog.exec():
            return dialog.getServerAddress()
        else:
            QMessageBox.critical(
                dialog,
                "Error",
                "<p>Dialog did not exit correctly</p>"
            )
            exit(1)

    def getAllNotes(self):
        return self.data['notes'].values()

    def getNote(self, id: int):
        return self.data['notes'][id]

    def addNote(self, title: str, text: str):
        note = self.req_handler.uploadNote(NoteBase(title=title, content=text))
        self.data['notes'][note.id] = note

    def removeNote(self, id: int):
        self.req_handler.deleteNote(id)
        del self.data['notes'][id]

    def editNote(self, id: int, text: str):
        self.data['notes'][id].content = text
        self.data['notes'][id] = self.req_handler.replaceNote(id, self.data['notes'][id])

    def getAllRecipes(self):
        return list(reversed(self.data['recipes'].values()))

    def getRecipe(self, dish: str):
        dish = dish.strip()
        
        if dish in self.data['recipes']:
            return self.data['recipes'][dish]

        recipe = self.req_handler.getRecipe(dish)

        if recipe is not None:
            self.data['recipes'][dish] = recipe

        return recipe

    def changeServer(self):
        self.data['server_address'] = self._get_server_address()

        self._save()

    def getImage(self, url: str):
        try:
            self.IMAGE_DIR.mkdir(exist_ok=True)
            filepath = (self.IMAGE_DIR / sha1(url.encode()).hexdigest()[:8]).resolve()
            if not filepath.exists():
                urlretrieve(url, filepath)
            return filepath
        except Exception as e:
            print(e)
            return None
