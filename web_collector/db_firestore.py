from app import app
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from app import app

if os.environ.get("DEVELOPMENT"):
    cred = credentials.Certificate("web-collector-db-b43111a86bb6.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
else:
    cred = credentials.Certificate("web-collector-db-b43111a86bb6.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()


def get_collection(collection_name):
    app.logger.info(collection_name)
    return db.collection(collection_name).stream()

def get_document_ref(collection_name, doc_id):
    #app.logger.info("%s %s", collection_name, doc_id)
    doc_ref = db.collection(collection_name).document(f"{doc_id}")
    return doc_ref


def insert_document(doc_ref, json_data):
    app.logger.info(f"Inserting document to {doc_ref}")
    app.logger.info(f"Document {json_data}")
    doc_ref.set(json_data)


def update_document(doc_ref, field_dict:dict):
    #app.logger.debug(f"Updating document {doc_ref}")
    if doc_ref.get().exists:
        app.logger.debug(f"Applying updates {field_dict}")
        doc_ref.update(field_dict)
    else:
        raise FileNotFoundError(f"Document not found")
