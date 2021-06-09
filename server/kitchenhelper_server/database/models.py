from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, PickleType, String
from sqlalchemy.orm import relationship

from .setup import Base


class User(Base):
    """
    The user record. It only contains the UUID of the user in text form,
    and the last used ID of user's notes.
    """

    __tablename__ = 'users'

    id = Column(String(length=36), primary_key=True, index=True)
    last_note_id = Column(Integer, nullable=False, default=0)

    notes = relationship('Note', back_populates='owner')


class Note(Base):
    """
    Note record, containing note data (title and content) and metadata facilitating
    note management, like last modification date etc.
    """

    __tablename__ = 'notes'

    owner_id = Column(String(length=36), ForeignKey('users.id'), primary_key=True, index=True)
    id = Column(Integer, primary_key=True, index=True)
    last_modified = Column(DateTime, nullable=False, default=lambda: datetime.now(tz=timezone.utc))
    title = Column(String, nullable=False)
    content = Column(String)

    owner = relationship('User', back_populates='notes')


class Recipe(Base):
    """
    Recipe record, containing all data gotten from `recipe-scrapers`, and URL for identification
    of previously stored recipes.
    """

    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False)
    total_time = Column(String)
    yields = Column(String)
    ingredients = Column(PickleType)
    instructions = Column(String)
    nutrients = Column(PickleType)
    image = Column(String)

    keywords = relationship('RecipeKeywords', back_populates='recipe')


class RecipeKeywords(Base):
    """
    Recipe keywords, used to reduce duplication of recipe records, if multiple sets of
    keywords yield the same search results.
    """

    __tablename__ = 'recipe_keywords'

    keywords = Column(String, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    
    recipe = relationship('Recipe', back_populates='keywords')
