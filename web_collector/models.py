from sqlalchemy import Integer, String, Column, Date, text
from sqlalchemy.ext.declarative import declarative_base
from web_collector.db import Sesson


Base = declarative_base()
Base.query = Sesson.query_property()


class HomesModel(Base):
    __tablename__ = "homes"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String)
    date_created = Column(String)
    date_found = Column(String)
    source = Column(String)
    web_id = Column(String)
    price = Column(Integer)
    image = Column(String)
    adv_url = Column(String)
    archived = Column(Integer, server_default=text('0'), nullable=False)
    comment = Column(String)

    def __repr__(self):
        return f"HomesModel {self.id} {self.title} {self.description} {self.date_created} {self.date_found} {self.source}"
