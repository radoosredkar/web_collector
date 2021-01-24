from datetime import datetime, timedelta
from web_collector.models import HomesModel
from flask import current_app as app

sesson = None


def db_add(item):
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
