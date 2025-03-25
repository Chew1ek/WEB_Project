import sqlalchemy
from .db_session import SqlAlchemyBase

class Films(SqlAlchemyBase):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
