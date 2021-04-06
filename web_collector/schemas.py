import graphene
from web_collector import log
from flask import current_app as app
from graphene import ObjectType, Mutation, String, Int, Field, List
from web_collector.db_firestore import db
import web_collector.db_firestore as db_firestore
import os
from config import settings

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
    type = String()

    def __init__(self, homes_dict, ident):
        self.id = ident
        for keys, values in homes_dict.items():
            # app.logger.info(keys + " " + str(values))
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

    def resolve_type(self, info):
        return f"{self.type}"


class UpdateComment(Mutation):
    class Arguments:
        ident = String()
        comment = String()

    home = graphene.Field(Home)

    def mutate(self, info, ident, comment):
        doc_ref = db_firestore.get_document_ref(settings.collections.homes, ident)
        doc = doc_ref.get()
        if doc.exists:
            db_firestore.update_document(doc_ref, {"comments": comment})
            home_dict = doc.to_dict()
            home = Home(home_dict, ident)
        else:
            home = None
        return UpdateComment(home=home)


class Mutation(ObjectType):
    update_comment = UpdateComment.Field()


class Query(ObjectType):
    home = graphene.Field(Home, ident=String())
    homes = List(Home, archived=Int(default_value=0))

    def resolve_home(self, info, ident):
        doc_ref = db_firestore.get_document_ref(settings.collections.homes, ident)
        return Home(doc_ref.get().to_dict(), ident)

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


schema = graphene.Schema(query=Query, mutation=Mutation)
