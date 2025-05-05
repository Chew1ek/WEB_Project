from sqlalchemy import *
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase



class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    seller_name = Column(String)
    description = Column(String)
    start_date = Column(DateTime)
    item_name = Column(String)
    price = Column(Integer)
    image_path = Column(String)
