import graphene
from web_collector.models import HomesModel
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import and_
from web_collector.db import Sesson
from web_collector import log
from flask import current_app as app


class Homes(SQLAlchemyObjectType):
    class Meta:
        model = HomesModel

class UpdateComment(graphene.Mutation):
    class Arguments:
        ident = graphene.Int()
        comment = graphene.String()

    home = graphene.Field(Homes)

    def mutate(root, info, ident, comment):
        query = Homes.get_query(info)
        if ident:
            session = Sesson()
            home: HomesModel = query.get(ident)
            home.comment = comment
            session.commit()
        return UpdateComment(home=home)


class MyMutations(graphene.ObjectType):
    update_comment = UpdateComment.Field()


class Query(graphene.ObjectType):
    homes = graphene.List(Homes)
    home = graphene.List(
        Homes,
        ident=graphene.Int(),
        title=graphene.String(),
        comment=graphene.String(),
        desc=graphene.String(),
        date_created=graphene.Date(),
        date_found=graphene.Date(),
        source=graphene.String(),
        web_id=graphene.String(),
        price_to=graphene.Float(),
        price_from=graphene.Float(),
        image=graphene.String(),
        adv_url=graphene.String(),
        archived=graphene.Int(),
    )

    def resolve_homes(self, info):
        query = Homes.get_query(info)
        return query.all()

    def resolve_home(self, info, **args):
        app.logger.debug("resolve_home %s", args)
        ident = args.get("ident")
        title = args.get("title")
        comment = args.get("comment")
        description = args.get("desc")
        archived = args.get("archived")
        price_from = args.get("price_from")
        price_to = args.get("price_to")

        flt = []
        if ident:
            app.logger.debug("Searching by id %s", ident)
            flt.append(HomesModel.id == ident)
        if title:
            flt.append((HomesModel.title.contains(title)))
        if comment:
            flt.append((HomesModel.comment.contains(comment)))
        if description:
            flt.append((HomesModel.description.contains(description)))
        if archived:
            flt.append(HomesModel.archived == 1)
        if not archived:
            flt.append(HomesModel.archived == 0)
        if price_to:
            flt.append((HomesModel.price <= price_to))
        if price_from:
            flt.append((HomesModel.price >= price_from))
        if price_from and price_to:
            flt.append(
                and_((HomesModel.price >= price_from), (HomesModel.price <= price_to))
            )

        query = Homes.get_query(info)

        sql = query.filter(*flt)
        app.logger.debug(sql)
        return sql.all()


schema = graphene.Schema(query=Query, mutation=MyMutations)
