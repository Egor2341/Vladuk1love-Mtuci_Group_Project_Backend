import sqlalchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from s3 import s3
from settings import settings
from .db_session import SqlAlchemyBase


class Photo(SqlAlchemyBase):
    __tablename__ = 'photos'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_login = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.login'), nullable=False)
    user_img = relationship('data.users.User', back_populates='photos', uselist=False)
    img_s3_location = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, img_s3_location: str):
        self.img_s3_location = img_s3_location

    @hybrid_property
    def s3_url(self):
        if self.img_s3_location is None:
            return None
        return s3.generate_link(bucket=settings.AWS_BUCKET, key=self.img_s3_location)
