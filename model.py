from sqlalchemy_serializer import SerializerMixin

import app

db = app.db


class User(db.Model):
    __tablename__ = 'USER'

    # serialize_only = ('id', 'nickname', 'gender', 'full_body_img_path')

    id = db.Column(db.String(50), primary_key=True)
    nickname = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(10), nullable=True)
    full_body_img_path = db.Column(db.String(255), nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'[USER] id: {self.id}, nickname: {self.nickname}, gender: {self.gender}, full_body_img_path: {self.full_body_img_path}'
