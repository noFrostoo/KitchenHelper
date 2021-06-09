from datetime import datetime, timezone
from typing import List, Optional
import uuid

from sqlalchemy.orm import Session

from kitchenhelper_server.api import schemas
from . import models


def create_user(db: Session) -> models.User:
    """
    Create a new user with a random UUID.
    """

    new_user = models.User(id=str(uuid.uuid4()))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_note(db: Session, note: schemas.NoteBase, user_id: str) -> models.Note:
    """
    Create a new note from the received data and save it under the user ID.
    """

    new_note = models.Note(**note.dict(), owner_id=user_id)
    new_note.id = db.query(models.User).filter(models.User.id == user_id).first().last_note_id + 1
    db.query(models.User).filter(models.User.id == user_id).update({models.User.last_note_id: new_note.id})
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


def create_recipe(db: Session, recipe: schemas.Recipe, keywords: str) -> models.Recipe:
    """
    An internal function used to cache found recipes, to speed up subsequent lookups of the
    same keywords
    """

    new_recipe = models.Recipe(**recipe.dict())
    db.add(new_recipe)
    db.flush()
    db.refresh(new_recipe)
    db.add(models.RecipeKeywords(keywords=' '.join(sorted(keywords.split(' '))), recipe_id=new_recipe.id))
    db.commit()
    return new_recipe


def replace_note(db: Session, note: schemas.NoteBase, id: int, user_id: str) -> Optional[models.Note]:
    """
    Replace note content with new content received from client.
    """

    note.id = id
    note.last_modified = note.last_modified or datetime.now(tz=timezone.utc)

    rows = db.query(models.Note) \
        .filter(models.Note.id == id, models.Note.owner_id == user_id) \
        .update(note.dict())
    db.commit()

    return models.Note(**note.dict()) if rows != 0 else None


def delete_note(db: Session, id: int, user_id: str) -> bool:
    rows = db.query(models.Note).filter(models.Note.id == id, models.Note.owner_id == user_id).delete()
    db.commit()
    return rows != 0


def get_notes_by_user(db: Session, user_id: str) -> List[models.Note]:
    """
    Get all notes owned by the user.
    """

    return db.query(models.Note) \
        .filter(models.Note.owner_id == user_id) \
        .order_by(models.Note.last_modified.desc()) \
        .all()


def get_note_by_id_and_user(db: Session, id: int, user_id: str) -> Optional[models.Note]:
    """
    Get a specific note owned by the user.
    """

    return db.query(models.Note).filter(models.Note.id == id, models.Note.owner_id == user_id).first()


def sync_notes(db: Session, user_id: str, notes: List[schemas.NoteBase]):
    """
    Sync notes received from client with those stored in database, replacing those
    with earlier modification date with those with later date.
    """

    for note in notes:
        last_m = note.last_modified or datetime.now()

        rows = db.query(models.Note).filter(
            models.Note.owner_id == user_id,
            models.Note.id == note.id,
            models.Note.last_modified < last_m
        ).update(note.dict())

        if not rows:
            present = db.query(models.Note).filter_by(owner_id=user_id, id=note.id).count()
            if not present:
                create_note(db, note, user_id)
    
    db.commit()


def get_recipe_by_keywords(db: Session, keywords: str) -> Optional[models.Recipe]:
    """
    Get already stored recipe by its keywords.
    """

    keywords = ' '.join(sorted(keywords.split(' ')))

    return db.query(models.Recipe) \
        .select_from(models.RecipeKeywords) \
        .join(models.RecipeKeywords.recipe) \
        .filter(models.RecipeKeywords.keywords == keywords) \
        .first()


def add_keywords_to_recipe(db: Session, id: int, keywords: str):
    """
    Add another set of keywords to a stored recipe.
    """

    keywords = ' '.join(sorted(keywords.split(' ')))
    db.add(models.RecipeKeywords(keywords=keywords, recipe_id=id))
    db.commit()
