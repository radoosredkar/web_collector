from datetime import datetime, timedelta
from web_collector.models import HomesModel
from app import app
import web_collector.db_firestore as db_firestore
import os
from config import settings
from enum import Enum


sesson = None

RECORD_TYPE = Enum(
    "RECORD_TYPE", "NEW_RECORD CANDIDATE FAVORITES NOT_CANDIDATE ARCHIVED"
)


def db_add(item):
    title = item.title
    desc = item.desc
    web_id = item.web_id
    if item and item.price:
        price = float(item.price.replace("€", "").replace(".", "").replace(",", "."))
    else:
        price = 0
    source = item.source
    date_created = item.date_created
    image = item.image
    adv_url = item.adv_url

    to_log = (title, web_id, price, source, date_created, image, adv_url)

    # app.logger.debug("working with record %s", to_log)
    # app.logger.debug("working with record id %s", web_id)

    doc_ref = db_firestore.get_document_ref(settings.collections.homes, web_id)
    doc = doc_ref.get()
    if not doc.exists:
        app.logger.debug("New record found %s", to_log)
        db_firestore.insert_document(
            doc_ref,
            {
                "title": title,
                "desc": desc,
                "price": price,
                "source": source,
                "date_created": date_created,
                "date_found": datetime.now(),
                "image": image,
                "adv_url": adv_url,
                "comments": "",
                "archived": 0,
                "type": RECORD_TYPE.NEW_RECORD.name,
            },
        )
        return True
    else:
        data_to_update = {"date_found": datetime.now()}
        db_firestore.update_document(doc_ref, data_to_update)
        return False  # Did not add


def db_add_sql(item):
    if not sesson:
        app.logger.error("Db session not set")
        pass
    title = item.title
    desc = item.desc
    web_id = item.web_id
    price = float(item.price.replace("€", "").replace(".", "").replace(",", "."))
    source = item.source
    date_created = item.date_created
    image = item.image
    adv_url = item.adv_url

    to_log = (title, web_id, price, source, date_created, image, adv_url)

    app.logger.debug("creating record {to_log} ")
    homesModel: HomesModel = HomesModel(
        title=title,
        description=desc,
        date_created=date_created,
        web_id=web_id,
        price=price,
        source=source,
        image=image,
        adv_url=adv_url,
    )

    existing_sr = (
        sesson.query(HomesModel).filter(HomesModel.web_id == f"{web_id}").first()
    )
    app.logger.debug(
        f"record {web_id} {'found' if existing_sr else 'not found' } in db"
    )
    if not existing_sr:
        app.logger.info("Adding {web_id} to db")
        sesson.add(homesModel)
        return True
    else:
        existing_sr.date_found = datetime.now()

    # update archived records if oldet than 5 days
    sesson.query(HomesModel).filter(
        HomesModel.date_found < (datetime.now() - timedelta(5))
    ).update(dict(archived=1))
    return False
