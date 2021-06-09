"""
The database configuration. Because of the small scale, the server uses
a SQLite database for simplicity.
"""


from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Path('data').mkdir(exist_ok=True)

SQLALCHEMY_DATABASE_URL = 'sqlite:///./data/db.sqlite'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
