import ipdb
import requests
import praw
import datetime
from models import HomesModel
from db import Sesson
import bs4
from bs4 import BeautifulSoup
from datetime import datetime

# import sentry_sdk
# sentry_sdk.init("https://007e055e5fe64e35b55b36140bf6b18d@o371271.ingest.sentry.io/5363923")


def db_add(item):
    title = item.title
    desc = item.desc
    web_id = item.web_id
    price = float(item.price.replace("€", "").replace(".", "").replace(",", "."))
    source = item.source
    date_created = item.date_created
    image = item.image
    adv_url = item.adv_url
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

    # print(f"X{created}X")
    existing_sr = (
        sesson.query(HomesModel).filter(HomesModel.web_id == f"{web_id}").first()
    )
    if not existing_sr:
        sesson.add(homesModel)
        return True
    else:
        existing_sr.date_found = datetime.now()
    return False


url_bolha = "https://www.bolha.com/index.php?ctl=search_ads&keywords=stanovanja&categoryId=9580&price[min]=98000&price[max]=140999&level0LocationId%5B26320%5D=26320&sort=new&page={page}"

url_nepremicnine = "https://www.nepremicnine.net/oglasi-prodaja/ljubljana-okolica/stanovanje/cena-od-100000-do-150000-eur,velikost-od-50-do-100-m2/{page}/"


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
                    link = item.find(class_="link")
                    if link:
                        name = link.get("name")
                        instance.__setattr__(self.attr, name)

                elif self.attr == "price":
                    instance.__setattr__(self.attr, " ".join(item.text.split()))
                elif self.attr == "date_created":
                    instance.__setattr__(
                        self.attr, datetime.strptime(item.text, "%d.%m.%Y.")
                    )
                elif self.attr == "image":
                    instance.__setattr__(self.attr, item["data-src"])
                elif self.attr == "adv_url":
                    instance.__setattr__(
                        self.attr, f'https://www.bolha.com{item["href"]}'
                    )
                else:
                    instance.__setattr__(self.attr, " ".join(item.text.split()))
                return instance.__getattribute__(self.attr)


class ExtractorDescNepremicnine(object):
    item = None
    """A data descriptor that extracts data from BeautifulSoup item"""

    def __init__(self, attr, class_):
        self.attr = attr
        self.class_ = class_

    def __get__(self, instance, owner):
        if instance.item:
            item = instance.item.find(class_=self.class_)
            if item:
                if self.attr == "price":
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
    title = ExtractorDesc("title", "entity-title")
    desc = ExtractorDesc("decs", "entity-description-main")
    date_created = ExtractorDesc("date_created", "date date--full")
    price = ExtractorDesc("price", "price price--hrk")
    currency = ExtractorDesc("currency", "currency")
    web_id = ExtractorDesc("web_id", "entity-title")
    image = ExtractorDesc("image", "entity-thumbnail-img")
    adv_url = ExtractorDesc("adv_url", "link")
    source = "Bolha"

    def __init__(self, item):
        self.__dict__["item"] = item

    def __setattr(self, attr, val):
        if attr == "title":
            self.title.item = self.item


class ParserNepremicnine:
    title = ExtractorDescNepremicnine("title", "title")
    desc = ExtractorDescNepremicnine("decs", "kratek")
    date_created = datetime.now()
    price = ExtractorDescNepremicnine("price", "cena")
    currency = ExtractorDescNepremicnine("currency", "currency")
    web_id = ExtractorDescNepremicnine("web_id", "oglas_container")
    image = ExtractorDescNepremicnine("image", "slika")
    adv_url = ExtractorDescNepremicnine("adv_url", "slika")
    source = "Nepremicnine"

    def __init__(self, item):
        self.__dict__["item"] = item

    def __setattr(self, attr, val):
        if attr == "title":
            self.title.item = self.item


def scrapp():
    new_items = 0
    for pageNum in range(1, 100):
        print(f"parsing page {pageNum}")
        page: requests.models.Response = requests.get(url_bolha.format(page=pageNum))
        soup: bs4.BeautifulSoup = BeautifulSoup(page.content, "html.parser")
        stop_element = soup.find(class_="brdr_top ad_item")
        if not stop_element:
            all_items = soup.find_all(class_="EntityList-item")
            print(f"{len(all_items)} items found")
            for item in all_items:
                parser: Parser = Parser(item)
                if parser.title and parser.desc:
                    # print("title", parser.title)
                    # print("desc", parser.desc)
                    # print("date", parser.date_created)
                    # print("price", parser.price)
                    # print("web_id", parser.web_id)
                    # print("image", parser.image)
                    # print("adv_url", parser.adv_url)
                    if db_add(parser):
                        new_items += 1
        else:
            print(f"Commiting to db {new_items} new items")
            break


def scrappNepremicnine():
    new_items = 0
    for pageNum in range(1, 10):
        print(f"parsing page {pageNum}")
        page: requests.models.Response = requests.get(
            url_nepremicnine.format(page=pageNum)
        )
        print(url_nepremicnine.format(page=pageNum))
        soup: bs4.BeautifulSoup = BeautifulSoup(page.content, "html.parser")
        all_items = soup.find_all(class_="oglas_container")
        if not all_items:
            break
        print(f"{len(all_items)} items found")
        for item in all_items:
            parser: ParserNepremicnine = ParserNepremicnine(item)
            if parser.title and parser.desc:
                parser.web_id = item["id"]
                # print("title", parser.title)
                # print("desc", parser.desc)
                # print("date", parser.date_created)
                # print("price", parser.price)
                # print("image", parser.image)
                # print("adv_url", parser.adv_url)
                if db_add(parser):
                    new_items += 1
    print(f"Commiting to db {new_items} new items")


sesson = Sesson()
if __name__ == "__main__":
    scrapp()
    sesson.commit()
    scrappNepremicnine()
    sesson.commit()
