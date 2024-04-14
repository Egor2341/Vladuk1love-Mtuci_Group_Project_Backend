import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Profile(SqlAlchemyBase):
    __tablename__ = 'profiles'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_login = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.login'), nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)

    user = relationship('data.users.User', back_populates='profile', uselist=False)
