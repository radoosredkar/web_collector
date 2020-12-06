from datetime import datetime, timedelta

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
