import graphene
from models import HomesModel
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import and_


class Homes(SQLAlchemyObjectType):
    class Meta:
        model = HomesModel


class Query(graphene.ObjectType):
    homes = graphene.List(Homes)
    home = graphene.List(
        Homes,
        title=graphene.String(),
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
        ident = args.get("ident")
        title = args.get("title")
        description = args.get("desc")
        archived = args.get("archived")
        price_from = args.get("price_from")
        price_to = args.get("price_to")

        flt = []
        if title:
            flt.append((HomesModel.title.contains(title)))
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
        if ident:
            return query.get(ident)
        else:
            sql = query.filter(*flt)
            print(sql)
            return sql.all()


schema = graphene.Schema(query=Query)
