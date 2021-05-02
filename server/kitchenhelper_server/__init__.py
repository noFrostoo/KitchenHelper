from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import uvicorn

from .api import schemas
from .database import crud, models
from .database.setup import SessionLocal, engine
from .web.recipes import find_recipe

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/users/register', response_model=str)
def register_user(db: Session = Depends(get_db)):
    return str(crud.create_user(db).id)


@app.get('/notes/{user_id}/{id}', response_model=schemas.Note)
def get_note(user_id: str, id: int, db: Session = Depends(get_db)):
    note = crud.get_note_by_id_and_user(db, id, user_id)
    if note is None:
        raise HTTPException(status_code=404, detail='Note not found')
    return note


@app.get('/notes/{user_id}', response_model=List[schemas.Note])
def get_all_notes(user_id: str, db: Session = Depends(get_db)):
    return crud.get_notes_by_user(db, user_id)


@app.post('/notes/{user_id}/new', response_model=schemas.Note)
def create_note(user_id: str, note: schemas.NoteBase, db: Session = Depends(get_db)):
    return crud.create_note(db, note, user_id)


@app.put('/notes/{user_id}/{id}', response_model=bool)
def replace_note(user_id: str, id: int, note: schemas.NoteBase, db: Session = Depends(get_db)):
    if not crud.replace_note(db, note, id, user_id):
        raise HTTPException(status_code=404, detail='Note not found')

    return True


@app.delete('/notes/{user_id}/{id}', response_model=bool)
def delete_note(user_id: str, id: int, db: Session = Depends(get_db)):
    return crud.delete_note(db, id, user_id)


@app.get('/recipes/{keywords}', response_model=schemas.Recipe)
def get_recipe(keywords: str, db: Session = Depends(get_db)):
    keywords = keywords.replace('+', ' ').lower()
    recipe = crud.get_recipe_by_keywords(db, keywords)

    if recipe is None:
        recipe = find_recipe(keywords)

        if recipe is None:
            raise HTTPException(status_code=404, detail='Could not find a recipe matching given keywords')

        crud.create_recipe(db, recipe)
    
    return recipe


def main():
    uvicorn.run('kitchenhelper_server:app', host='0.0.0.0', port=8080, reload=True)
