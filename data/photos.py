import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Photo(SqlAlchemyBase):
    __tablename__ = 'photos'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_login = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.login'), nullable=False)
    img = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    user_img = relationship('data.users.User', back_populates='photos', uselist=False)
