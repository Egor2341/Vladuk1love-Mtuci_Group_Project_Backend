import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Photo(SqlAlchemyBase):
    __tablename__ = 'photos'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_login = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.login'), nullable=False, unique=True)
    img = sqlalchemy.Column(sqlalchemy.Text, nullable=False, unique=True)
    name = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    mimetype = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_imgs = relationship('User', back_populates='photos')