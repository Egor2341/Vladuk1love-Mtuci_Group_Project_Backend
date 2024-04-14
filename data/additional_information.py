import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Info(SqlAlchemyBase):
    __tablename__ = 'additional_information'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_login = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.login'), nullable=False, unique=True)
    about_me = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    interests = sqlalchemy.Column(sqlalchemy.Text)
    z = sqlalchemy.Column(sqlalchemy.String)
    height = sqlalchemy.Column(sqlalchemy.Integer)
    education = sqlalchemy.Column(sqlalchemy.String)

    user_info = relationship('data.users.User', back_populates='add_info', uselist=False)
