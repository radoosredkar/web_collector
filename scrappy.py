import ipdb
from .db import Sesson
from .log import logger
from . import log
import sys
from . import ParserBolha as bolha
from .import ParserNepremicnine as nepremicnine
from . import scrappy_db as db

# import sentry_sdk
# sentry_sdk.init("https://007e055e5fe64e35b55b36140bf6b18d@o371271.ingest.sentry.io/5363923")
log.setLoggingFile(__name__)
log.setStreamHandler(None)

url_bolha = "https://www.bolha.com/index.php?ctl=search_ads&keywords=stanovanja&categoryId=9580&price[min]=98000&price[max]=140999&level0LocationId%5B26320%5D=26320&sort=new&page={page}"

url_nepremicnine = "https://www.nepremicnine.net/oglasi-prodaja/ljubljana-okolica/stanovanje/cena-od-100000-do-150000-eur,velikost-od-50-do-100-m2/{page}/"


def refresh():
    db.sesson = Sesson()
    all_changed_items = 0
    all_changed_items = all_changed_items + bolha.scrapp(url_bolha)
    all_changed_items = all_changed_items + nepremicnine.scrapp(url_nepremicnine)
    db.sesson.commit()
    return f"{str(all_changed_items)}"


if __name__ == "__main__":
    all_changed_items = refresh()
    print(all_changed_items)
