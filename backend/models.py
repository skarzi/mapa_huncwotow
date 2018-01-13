from flask import current_app
from requests_oauthlib import OAuth1Session
from sqlalchemy.orm.exc import NoResultFound

from .extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_or_create(cls, **kwargs):
        defaults = kwargs.pop("defaults", {})
        try:
            item = cls.query.filter_by(**kwargs).one()
        except NoResultFound:
            kwargs.update(defaults)
            item = cls(**kwargs).save()
        return item

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def serialize(self):
        return {key: getattr(self, key) for key in self.__mapper__.c.keys()}


class POIs(BaseModel):
    __tablename__ = 'pois'

    name = db.Column(db.String(128))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    type = db.Column(db.String(32), default="")
    floor = db.Column(db.String(16))


class Users(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    app_hash = db.Column(db.String)
    oauth_token = db.Column(db.String, default=None)
    oauth_token_secret = db.Column(db.String, default=None)
    oauth_verifier = db.Column(db.String, default=None)

    def is_authorized(self):
        return bool(self.oauth_token) and bool(
            self.oauth_token_secret) and bool(self.oauth_verifier)

    def get_classes(self):
        auth = OAuth1Session(
            current_app.config['USOS_CONSUMER_KEY'],
            current_app.config['USOS_CONSUMER_SECRET'],
            resource_owner_key=self.oauth_token,
            resource_owner_secret=self.oauth_token_secret,
            verifier=self.oauth_verifier
        )
        response = auth.get(
            current_app.config['USOS_TIMETABLE_URL'],
            params="fields=room_number|name|start_time"
        ).json()
        first_classes = response[0]
        date, time = first_classes["start_time"].split()
        time = time[:-3]
        return {
            "name": first_classes["name"]["pl"],
            "room": first_classes["room_number"],
            "time": time
        }
