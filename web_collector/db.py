from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
import os
from config import settings

basedir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.abspath(basedir + f"/{settings.db.path}/{settings.db.name}")
#engine = create_engine("sqlite:///" + file_path, echo=False)
engine = create_engine(settings.db.url)


Sesson = scoped_session(sessionmaker(bind=engine))
