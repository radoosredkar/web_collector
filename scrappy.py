from datetime import datetime
from random import randrange
from web_collector.scrapper import ParserBolha as bolha
from web_collector.scrapper import ParserNepremicnine as nepremicnine
from flask import current_app as app
from config import settings
import web_collector.db_firestore as db_firestore
from web_collector.scrapper.scrappy_db import RECORD_TYPE as RECORD_TYPE
import push


# import sentry_sdk
# sentry_sdk.init("https://007e055e5fe64e35b55b36140bf6b18d@o371271.ingest.sentry.io/5363923")

URL_BOLHA = [
    "https://www.bolha.com/index.php?ctl=search_ads&keywords=stanovanja&categoryId=9580&price[min]=98000&price[max]=200000&level0LocationId%5B26320%5D=26320&sort=new&page={page}",
]

URL_NEPREMICNINE = [
    "https://www.nepremicnine.net/oglasi-prodaja/ljubljana-mesto/stanovanje/cena-do-200000-eur,velikost-od-50-do-100-m2/{page}/",
    "https://www.nepremicnine.net/oglasi-prodaja/ljubljana-okolica/stanovanje/cena-od-100000-do-200000-eur,velikost-od-50-do-150-m2/{page}/",
]


def refresh(client):
    now = datetime.now()
    document_id = now.strftime("%Y%m%d")
    entry_id = now.strftime("%H%M%S")

    doc_ref = db_firestore.get_document_ref(
        settings.collections.logs, "refresh_" + document_id
    )
    doc = doc_ref.get()
    if not doc.exists:
        document = {entry_id: {"action": "refresh", "datetime": now, "client": client}}
        db_firestore.insert_document(doc_ref, document)
    else:
        document = {entry_id: {"action": "refresh", "datetime": now, "client": client}}
        db_firestore.update_document(doc_ref, document)

    app.logger.info("Refresh triggered")

    all_changed_items = 0
    app.logger.info("Refreshing bolha")
    for url in URL_BOLHA:
        app.logger.info(f"Applying filter {url}")
        all_changed_items = all_changed_items + bolha.scrapp(url)
    app.logger.debug(f"Bolha refreshed {all_changed_items}")

    app.logger.info("Refreshing nepremicnine")
    for url in URL_NEPREMICNINE:
        app.logger.info(f"Applying filter {url}")
        all_changed_items = all_changed_items + nepremicnine.scrapp(url)
    app.logger.debug(f"Nepremicnine refreshed {all_changed_items}")

    db_firestore.update_document(doc_ref, {"changed_items": all_changed_items})

    app.logger.info(f"Refresh finished {str(all_changed_items)}")
    if all_changed_items > 0:
        app.logger.info("Sending push notification")
        push.push(f"{all_changed_items} found!")
    return all_changed_items


def archieve():
    all_archieved_items = 0
    all_deleted_items = 0
    now = datetime.now()

    document_id = now.strftime("%Y%m%d")
    entry_id = now.strftime("%H%M%S")

    homes_coll = db_firestore.get_collection(settings.collections.homes)

    doc_ref = db_firestore.get_document_ref(
        settings.collections.logs, "archieve_" + document_id
    )
    doc = doc_ref.get()
    if not doc.exists:
        document = {entry_id: {"action": "archieve", "datetime": now}}
        db_firestore.insert_document(doc_ref, document)
    else:
        document = {"action": "archieve", "datetime": now}
        db_firestore.insert_document(doc_ref, document)

    app.logger.debug("Checking for documents to archieve")
    for home in homes_coll:
        parsed = home.to_dict()
        timedelta = now - parsed["date_found"].replace(tzinfo=None)
        # app.logger.info("timedelta %s,%s", timedelta.days, settings.db.age_to_archive_days)
        if (
            timedelta.days > settings.db.age_to_archive_days
            and parsed["type"] != RECORD_TYPE.ARCHIVED.name
        ):
            app.logger.debug("Archieving document with timedelta %s", timedelta)
            db_firestore.update_document(
                home.reference, {"type": RECORD_TYPE.ARCHIVED.name, "archieved": now}
            )
            all_archieved_items = all_archieved_items + 1
        elif timedelta.days > 10 and parsed["type"] == RECORD_TYPE.ARCHIVED.name:
            app.logger.debug("Deleting document with timedelta %s", timedelta)
            db_firestore.delete_document(home.reference)
            all_deleted_items = all_deleted_items + 1
            # delete from collection
    db_firestore.update_document(
        doc_ref,
        {"archieved_items": all_archieved_items, "deleted_items": all_deleted_items},
    )
    app.logger.debug(f"Archieved {all_archieved_items} documents")
    app.logger.debug(f"Deleted {all_deleted_items} documents")
    return all_archieved_items


if __name__ == "__main__":
    all_changed_items = refresh()
    print(all_changed_items)
