import json
import requests
from typing import Iterable, Optional
from urllib.parse import urljoin, quote

from .schemas import Note, NoteBase, Recipe

class RequestHandler:
    def __init__(self, server_address: str, user_id: Optional[str] = None):
        self.base_url = f'http://{server_address}'
        self.user_id = user_id

    def _check_user(self):
        if self.user_id is None:
            raise Exception('User has not been registered!')

    def registerUser(self):
        response = requests.post(urljoin(self.base_url, '/users/register'))
        response.raise_for_status()
        self.user_id = response.json()
        return response.json()

    def getNotes(self):
        self._check_user()
        response = requests.get(urljoin(self.base_url, f'/notes/{self.user_id}'))
        response.raise_for_status()
        return [Note.parse_obj(note) for note in response.json()]

    def syncNotes(self, notes: Iterable[NoteBase]):
        self._check_user()
        data = json.dumps([n.dict() for n in notes])
        response = requests.post(urljoin(self.base_url, f'/notes/{self.user_id}'), data=data)
        response.raise_for_status()
        return [Note.parse_obj(note) for note in response.json()]

    def getNote(self, note_id: int):
        self._check_user()
        response = requests.get(urljoin(self.base_url, f'/notes/{self.user_id}/{note_id}'))
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return Note.parse_obj(response.json())

    def uploadNote(self, note: NoteBase):
        self._check_user()
        response = requests.post(
            urljoin(self.base_url, f'/notes/{self.user_id}/new'),
            data=note.json()
        )
        response.raise_for_status()
        return Note.parse_obj(response.json())

    def replaceNote(self, note_id: int, note: NoteBase):
        self._check_user()
        response = requests.put(
            urljoin(self.base_url, f'/notes/{self.user_id}/{note_id}'),
            data=note.json()
        )
        response.raise_for_status()
        return Note.parse_obj(response.json())

    def deleteNote(self, note_id: int):
        self._check_user()
        response = requests.delete(urljoin(self.base_url, f'/notes/{self.user_id}/{note_id}'))
        response.raise_for_status()
        return response.json()

    def getRecipe(self, dish):
        self._check_user()
        response = requests.get(urljoin(self.base_url, f'/recipes/{quote(dish)}'))
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return Recipe.parse_obj(response.json())
