from sqlalchemy import Integer, String, Column, Date, text, Text
from sqlalchemy.ext.declarative import declarative_base
from web_collector.db import Sesson


Base = declarative_base()
Base.query = Sesson.query_property()


class HomesModel(Base):
    __tablename__ = "homes"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), index=True)
    description = Column(Text(10000))
    date_created = Column(String(50))
    date_found = Column(String(50))
    source = Column(String(20))
    web_id = Column(String(20))
    price = Column(Integer)
    image = Column(Text(10000))
    adv_url = Column(String(500))
    archived = Column(Integer, server_default=text("0"), nullable=False)
    comment = Column(Text(20000))

    def __repr__(self):
        return f"HomesModel {self.id} {self.title} {self.description} {self.date_created} {self.date_found} {self.source}"
