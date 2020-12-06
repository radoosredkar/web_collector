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
