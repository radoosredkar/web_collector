import sys
from web_collector.scrapper import ParserBolha as bolha
from web_collector.scrapper import ParserNepremicnine as nepremicnine
from flask import current_app as app
from web_collector.db_firestore import db
from config import settings
import web_collector.db_firestore as db_firestore
from web_collector.scrapper.scrappy_db import RECORD_TYPE as RECORD_TYPE
import push

from datetime import datetime
from random import randrange


# import sentry_sdk
# sentry_sdk.init("https://007e055e5fe64e35b55b36140bf6b18d@o371271.ingest.sentry.io/5363923")

url_bolha = "https://www.bolha.com/index.php?ctl=search_ads&keywords=stanovanja&categoryId=9580&price[min]=98000&price[max]=200000&level0LocationId%5B26320%5D=26320&sort=new&page={page}"

url_nepremicnine = "https://www.nepremicnine.net/oglasi-prodaja/ljubljana-okolica/stanovanje/cena-od-100000-do-200000-eur,velikost-od-50-do-150-m2/{page}/"


def refresh(client):
    now = datetime.now()
    document_id = now.strftime("%Y%m%d-%H%M%S") + str(randrange(10000, 99999))

    doc_ref = db_firestore.get_document_ref(settings.collections.logs, document_id)

    document = {"action": "refresh", "datetime": now, "client": client}
    db_firestore.insert_document(doc_ref, document)

    app.logger.info("Refresh triggered")

    all_changed_items = 0
    app.logger.info("Refreshing bolha")
    all_changed_items = all_changed_items + bolha.scrapp(url_bolha)
    app.logger.debug(f"Bolha refreshed {all_changed_items}")

    app.logger.info("Refreshing nepremicnine")
    all_changed_items = all_changed_items + nepremicnine.scrapp(url_nepremicnine)
    app.logger.debug(f"Nepremicnine refreshed {all_changed_items}")

    db_firestore.update_document(doc_ref, {"changed_items": all_changed_items})
    homes_coll = db_firestore.get_collection(settings.collections.homes)
    for home in homes_coll:
        parsed = home.to_dict()
        timedelta = now - parsed["date_found"].replace(tzinfo=None)
        # app.logger.info("timedelta %s,%s", timedelta.days, settings.db.age_to_archive_days)
        if timedelta.days > settings.db.age_to_archive_days:
            app.logger.debug("Archieving document with timedelta %s", timedelta)
            db_firestore.update_document(
                home.reference, {"type": RECORD_TYPE.ARCHIVED.name}
            )

    app.logger.info(f"Refresh finished {str(all_changed_items)}")
    if all_changed_items > 0:
        app.logger.info("Sending push notification")
        push.push(f"{all_changed_items} found!")
    return all_changed_items


if __name__ == "__main__":
    all_changed_items = refresh()
    print(all_changed_items)
