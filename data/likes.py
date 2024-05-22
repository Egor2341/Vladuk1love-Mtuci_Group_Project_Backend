import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase

likes_to_likes_association_table = sqlalchemy.Table(
    'likes_to_likes_association_table',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('my_likes_id', sqlalchemy.ForeignKey('my_likes.id'), primary_key=True),
    sqlalchemy.Column('who_liked_me_id', sqlalchemy.ForeignKey('who_liked_me.id'), primary_key=True)
)


class MyLikes(SqlAlchemyBase):
    __tablename__ = 'my_likes'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_login = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.login'), nullable=False)
    who_i_liked = sqlalchemy.Column(sqlalchemy.String)
    who_liked_me = relationship('WhoLikedMe', secondary=likes_to_likes_association_table,
                                back_populates='who_i_liked',
                                uselist=True)
    user_likes = relationship('data.users.User', back_populates='my_likes', uselist=False)


class WhoLikedMe(SqlAlchemyBase):
    __tablename__ = 'who_liked_me'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_login = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.login'))
    user_who_was_liked = sqlalchemy.Column(sqlalchemy.String)
    who_i_liked = relationship('MyLikes', secondary=likes_to_likes_association_table,
                               back_populates='who_liked_me', uselist=True)
    user_liked_me = relationship('data.users.User', back_populates='who_liked_me', uselist=False)
