from app import app
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

if os.environ.get("DEVELOPMENT"):
    cred = credentials.Certificate('web-collector-db-a5211541cd82.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
else:
    cred = credentials.Certificate('web-collector-db-a5211541cd82.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()


#Sesson = scoped_session(sessionmaker(bind=engine))
