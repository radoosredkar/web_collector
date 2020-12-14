from datetime import datetime, timedelta
import bs4
from bs4 import BeautifulSoup
import requests
from .log import logger
from . import log
from . import scrappy_db as db

log.setLoggingFile(__name__)
log.setStreamHandler(None)


class ExtractorDesc(object):
    item = None
    """A data descriptor that extracts data from BeautifulSoup item"""

    def __init__(self, attr, class_):
        self.attr = attr
        self.class_ = class_

    def __get__(self, instance, owner):
        if instance.item:
            item = instance.item.find(class_=self.class_)
            if item:
                if self.attr == "web_id":
                    instance.__setattr__(self.attr, (item["id"]))
                elif self.attr == "price":
                    instance.__setattr__(self.attr, (item.text.split()[0]))
                elif self.attr == "date_created":
                    instance.__setattr__(
                        self.attr, datetime.strptime(item.text, "%d.%m.%Y.")
                    )
                elif self.attr == "image":
                    instance.__setattr__(
                        self.attr, item.find("img", recursive=False)["data-src"]
                    )
                elif self.attr == "adv_url":
                    instance.__setattr__(
                        self.attr, f'https://www.nepremicnine.net{item["href"]}'
                    )
                else:
                    instance.__setattr__(self.attr, " ".join(item.text.split()))
                return instance.__getattribute__(self.attr)


class Parser:
    title = ExtractorDesc("title", "title")
    desc = ExtractorDesc("decs", "kratek")
    date_created = datetime.now()
    price = ExtractorDesc("price", "cena")
    currency = ExtractorDesc("currency", "currency")
    web_id = ExtractorDesc("web_id", "oglas_container")
    image = ExtractorDesc("image", "slika")
    adv_url = ExtractorDesc("adv_url", "slika")
    source = "Nepremicnine"

    def __init__(self, item):
        self.__dict__["item"] = item

    def __setattr(self, attr, val):
        if attr == "title":
            self.title.item = self.item


def scrapp(url:str):
    new_items = 0
    for pageNum in range(1, 10):
        logger.info(f"parsing page {pageNum}")
        # print(f"parsing page {pageNum}")
        page: requests.models.Response = requests.get(
            url.format(page=pageNum)
        )
        logger.debug(url.format(page=pageNum))
        soup: bs4.BeautifulSoup = BeautifulSoup(
            page.content, "html.parser", from_encoding="utf-8"
        )
        all_items = soup.find_all(class_="oglas_container")
        if not all_items:
            break
        logger.info(f"{len(all_items)} items found")
        for item in all_items:
            parser: Parser = Parser(item)
            if parser.title and parser.desc:
                parser.web_id = item["id"]

                parser.image = parser.image.replace(
                    "sIonep", "slonep"
                )  # quickfix because of Beautifuls soup's invalid parsing of l
                if db.db_add(parser):
                    new_items += 1
    logger.info(f"Commiting to db {new_items} new items")
    return new_items
