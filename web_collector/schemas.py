import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import and_
from web_collector import log
from flask import current_app as app
from graphene import ObjectType, String, Int, Field, List
from web_collector.db_firestore import db
import os
if os.environ.get("DEVELOPMENT"):
    homes_collection_name = "homes_dev"
else:
    homes_collection_name = "homes"


class Home(ObjectType):
    id = String()
    title = String()
    description = String()
    source = String()
    price = String()
    adv_url = String()
    date_created = String()
    date_found = String()
    image = String()
    archived = Int()
    comments = String()

    def __init__(self, homes_dict, ident):
        self.id = ident
        for keys, values in homes_dict.items():
            #app.logger.info(keys + " " + str(values))
            setattr(self, keys, values)

    def resolve_id(self, info):
        return f"{self.id}"

    def resolve_title(self, info):
        return f"{self.title}"

    def resolve_description(self, info):
        return f"{self.desc}"

    def resolve_source(self, info):
        return f"{self.source}"

    def resolve_price(self, info):
        return f"{self.price}"

    def resolve_adv_url(self, info):
        return f"{self.adv_url}"

    def resolve_date_created(self, info):
        return f"{self.date_created}"


    def resolve_image(self, info):
        return f"{self.image}"

    def resolve_archived(self, info):
        return f"{self.archived}"

    def resolve_comments(self, info):
        return f"{self.comments}"


class Query(ObjectType):
    home = graphene.Field(Home)
    homes = List(Home, archived=Int(default_value=0))

    def resolve_home(self, info):
        return Home(title="test", ident=123)

    def resolve_homes(self, info, archived):
        homes_ref = db.collection(homes_collection_name)
        docs = homes_ref.stream()
        homes = []
        for doc in docs:
            home_dict = doc.to_dict()
            # app.logger.info(home_dict)
            home = Home(home_dict, doc.id)
            if home.archived == archived:
                homes.append(home)
        return homes


schema = graphene.Schema(query=Query)
