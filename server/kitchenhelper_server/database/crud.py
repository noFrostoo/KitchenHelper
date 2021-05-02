from typing import Iterable, List, Optional, Union
import uuid

from sqlalchemy.orm import Session

from kitchenhelper_server.api import schemas
from . import models


def create_user(db: Session) -> models.User:
    new_user = models.User(id=str(uuid.uuid4()))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_note(db: Session, note: schemas.NoteBase, user_id: str) -> models.Note:
    new_note = models.Note(**note.dict(), owner_id=user_id)
    new_note.id = db.query(models.User).filter(models.User.id == user_id).first().last_note_id + 1
    db.query(models.User).filter(models.User.id == user_id).update({models.User.last_note_id: new_note.id})
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


def create_recipe(db: Session, recipe: schemas.Recipe) -> models.Recipe:
    new_recipe = models.Recipe(**recipe.dict())
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe


def replace_note(db: Session, note: schemas.NoteBase, id: int, user_id: str) -> bool:
    note.id = id
    rows = db.query(models.Note) \
        .filter(models.Note.id == id, models.Note.owner_id == user_id) \
        .update(note.dict())
    db.commit()
    return rows != 0


def delete_note(db: Session, id: int, user_id: str) -> bool:
    rows = db.query(models.Note).filter(models.Note.id == id, models.Note.owner_id == user_id).delete()
    db.commit()
    return rows != 0


def get_notes_by_user(db: Session, user_id: str) -> List[models.Note]:
    return db.query(models.Note).filter(models.Note.owner_id == user_id).all()


def get_note_by_id_and_user(db: Session, id: int, user_id: str) -> Optional[models.Note]:
    return db.query(models.Note).filter(models.Note.id == id, models.Note.owner_id == user_id).first()


def get_recipe_by_keywords(db: Session, keywords: Union[str, Iterable[str]]) -> Optional[models.Recipe]:
    if type(keywords) == str:
        keywords = ' '.join(sorted(keywords.split(' ')))
    else:
        keywords = ' '.join(sorted(keywords))

    return db.query(models.Recipe).filter(models.Recipe.keywords == keywords).first()
