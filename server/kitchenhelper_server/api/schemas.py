from typing import List, Optional

from pydantic import BaseModel


class Note(BaseModel):
    id: Optional[int]
    title: str
    content: Optional[str]

    class Config:
        orm_mode = True


class User(BaseModel):
    id: str
    notes: List[Note]

    class Config:
        orm_mode = True


class Recipe(BaseModel):
    id: Optional[int]
    keywords: str
    title: str
    ingredients: Optional[str]
    instructions: Optional[str]
    total_time: Optional[str]
    image: Optional[bytes]

    class Config:
        orm_mode = True
