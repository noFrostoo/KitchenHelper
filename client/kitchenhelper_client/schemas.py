from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class NoteBase(BaseModel):
    id: Optional[int]
    last_modified: Optional[datetime]
    title: str
    content: Optional[str]


class Note(NoteBase):
    id: int
    last_modified: datetime


class User(BaseModel):
    id: str
    last_note_id: int = 0
    notes: List[Note]


class Recipe(BaseModel):
    url: str
    title: str
    total_time: Optional[str]
    yields: Optional[str]
    ingredients: List[str]
    instructions: Optional[str]
    nutrients: Dict[str, str]
    image: Optional[str]
