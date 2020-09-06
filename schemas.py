import graphene
from models import HomesModel
from graphene_sqlalchemy import SQLAlchemyObjectType


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
        price=graphene.Float(),
        image=graphene.String(),
        adv_url=graphene.String(),
    )

    def resolve_homes(self, info):
        query = Homes.get_query(info)
        return query.all()

    def resolve_home(self, info, **args):
        ident = args.get("ident")
        title = args.get("title")
        description = args.get("desc")

        flt = []
        if title:
            flt.append((HomesModel.title.contains(title)))
        if description:
            flt.append((HomesModel.description.contains(description)))

        query = SubReddit.get_query(info)
        if ident:
            return query.get(ident)
        else:
            sql = query.filter(*flt)
            print(sql)
            return sql.all()


schema = graphene.Schema(query=Query)
