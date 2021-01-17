
from datetime import datetime, timedelta
import bs4
from bs4 import BeautifulSoup
import requests
from web_collector.scrapper import scrappy_db as db
from flask import current_app as app


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


from datadog import initialize, statsd

options = {"statsd_host": "127.0.0.1", "statsd_port": 8125}

initialize(**options)


def scrapp(url: str):
    new_items = 0
    for pageNum in range(1, 100):
        # app.logger.info("A" * 200)
        app.logger.info(f"parsing page {pageNum}")
        # print(f"parsing page {pageNum}")
        page: requests.models.Response = requests.get(url.format(page=pageNum))
        soup: bs4.BeautifulSoup = BeautifulSoup(page.content, "html.parser")
        stop_element = soup.find(class_="brdr_top ad_item")
        if not stop_element:
            all_items = soup.find_all(class_="EntityList-item")
            app.logger.debug(f"{len(all_items)} items found")
            for item in all_items:
                statsd.increment("example_metric.increment", tags=["environment:bolha"])
                parser: Parser = Parser(item)
                if parser.title and parser.desc:
                    app.logger.debug(f" {parser} item found.")
                    if db.db_add(parser):
                        app.logger.info(f"New record added {parser}")
                        statsd.increment(
                            "example_metric.increment", tags=["environment:db_bolha"]
                        )
                        new_items += 1
        else:
            app.logger.info(f"Commiting to db {new_items} new items")
            break
    app.logger.info(f"Commiting to db {new_items} new items")
    return new_items
