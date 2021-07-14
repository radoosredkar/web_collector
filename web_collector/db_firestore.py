from app import app
import datetime
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
    # app.logger.info("%s %s", collection_name, doc_id)
    doc_ref = db.collection(collection_name).document(f"{doc_id}")
    return doc_ref


def insert_document(doc_ref, json_data):
    app.logger.info(f"Inserting document to {doc_ref}")
    app.logger.info(f"Document {json_data}")
    doc_ref.set(json_data)


def update_document(doc_ref, field_dict: dict):
    # app.logger.debug(f"Updating document {doc_ref}")
    if doc_ref.get().exists:
        app.logger.debug(f"Applying updates {field_dict}")
        doc_ref.update(field_dict)
    else:
        raise FileNotFoundError(f"Document not found")


def delete_document(doc_ref):
    # app.logger.debug(f"Updating document {doc_ref}")
    if doc_ref.get().exists:
        app.logger.debug("Deleting document")
        doc_ref.delete()
    else:
        raise FileNotFoundError("Document not found")


def get_latest_refresh(collection_name):
    now = datetime.datetime.now()
    document_id = now.strftime("%Y%m%d")
    #document_id = "20210703"
    app.logger.info(f"collection_name: {collection_name}, document_id:{document_id}")
    current_refresh_doc = get_document_ref(collection_name, f"refresh_{document_id}")
    #app.logger.debug(current_refresh_doc.get().to_dict())
    all_times = current_refresh_doc.get().to_dict()
    if all_times:
        all_times=list(all_times)
        all_times.sort()
        time = all_times[-1]
        return f"{document_id[0:4]}-{document_id[4:6]}-{document_id[6:8]}T{time[0:2]}:{time[2:4]}:{time[4:6]}"
    # result_stream = (
    # db.collection(collection_name)
    # .order_by("datetime", direction="DESCENDING")
    # .limit(1)
    # .stream()
    # )
    # result_date = next(result_stream).to_dict()
    # return result_date
