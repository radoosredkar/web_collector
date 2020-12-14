from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.abspath(basedir + "/migrations/app.db")
engine = create_engine("sqlite:///" + file_path, echo=False)


Sesson = scoped_session(sessionmaker(bind=engine))
