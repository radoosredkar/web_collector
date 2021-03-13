from datetime import datetime, timedelta
from web_collector.models import HomesModel
from app import app
import web_collector.db_firestore as db_firestore
import os
from config import settings


sesson = None

def db_add(item):
    title = item.title
    desc = item.desc
    web_id = item.web_id
    price = float(item.price.replace("€", "").replace(".", "").replace(",", "."))
    source = item.source
    date_created = item.date_created
    image = item.image
    adv_url = item.adv_url

    to_log = (title, web_id, price, source, date_created, image, adv_url)

    app.logger.debug("working with record %s ", to_log)

    doc_ref = db_firestore.get_document_ref(settings.collections.logs, web_id)
    doc = doc_ref.get()

    if not doc.exists:
        app.logger.debug("creating document %s ", web_id)
        doc_ref.set({
           u'title': title,
           u'desc': desc,
           u'price': price,
           u'source': source,
           u'date_created': date_created,
           u'date_found': datetime.now(),
           u'image': image,
           u'adv_url': adv_url,
           u'comments': '',
           u'archived': 0
        })
    else:
        app.logger.debug("document %s found", web_id)
        doc_ref.update({
           u'date_found': datetime.now()
        })


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

    app.logger.debug("creating record %s ", to_log)
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
