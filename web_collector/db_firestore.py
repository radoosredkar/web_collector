from app import app
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from app import app

if os.environ.get("DEVELOPMENT"):
    cred = credentials.Certificate("web-collector-db-a5211541cd82.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
else:
    cred = credentials.Certificate("web-collector-db-a5211541cd82.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()


def get_document_ref(collection_name, doc_id):
    app.logger.info(collection_name, doc_id)
    doc_ref = db.collection(collection_name).document(f"{doc_id}")
    return doc_ref
