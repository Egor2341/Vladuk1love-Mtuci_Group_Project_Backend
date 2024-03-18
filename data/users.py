import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_jwt_extended import create_access_token
from datetime import timedelta


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # def __init__(self, **kwargs):
    #     self.name = kwargs.get('name')
    #     self.email = kwargs.get("email")
    #     self.hashed_password = generate_password_hash(kwargs.get('hashed_password'))
    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta
        )
        return token

    # @classmethod
    # def authenticate(cls, email, password):
    #     user = cls.query.filter(cls.email == email).one()
    #     if not check_password_hash(password, user.hashed_password):
    #         raise Exception('No user with this password')
    #     return user

    def __repr__(self):
        return f"<User> {self.email}"

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
