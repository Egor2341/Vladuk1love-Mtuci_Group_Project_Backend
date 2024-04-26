import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Preference(SqlAlchemyBase):
    __tablename__ = 'preferences'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_login = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.login'), nullable=False, unique=True)
    age_pref = sqlalchemy.Column(sqlalchemy.String(50))
    height_pref = sqlalchemy.Column(sqlalchemy.String(50))
    weight_pref = sqlalchemy.Column(sqlalchemy.String(50))
    habbits = sqlalchemy.Column(sqlalchemy.String(50))

    user_pref = relationship('data.users.User', back_populates='preferences', uselist=False)
