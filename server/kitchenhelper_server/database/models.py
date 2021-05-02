from sqlalchemy import Column, ForeignKey, Integer, PickleType, String
from sqlalchemy.orm import relationship

from .setup import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(String(length=36), primary_key=True, index=True)
    last_note_id = Column(Integer, nullable=False, default=0)

    notes = relationship('Note', back_populates='owner')


class Note(Base):
    __tablename__ = 'notes'

    owner_id = Column(String(length=36), ForeignKey('users.id'), primary_key=True, index=True)
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    content = Column(String)

    owner = relationship('User', back_populates='notes')


class Recipe(Base):
    __tablename__ = 'recipes'

    keywords = Column(String, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    total_time = Column(String)
    yields = Column(String)
    ingredients = Column(PickleType)
    instructions = Column(String)
    nutrients = Column(PickleType)
    image = Column(String)
