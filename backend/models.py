from sqlalchemy.orm.exc import NoResultFound

from .extensions import db


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    app_hash = db.Column(db.String)
    oauth_token = db.Column(db.String, default=None)
    oauth_token_secret = db.Column(db.String, default=None)
    oauth_verifier = db.Column(db.String, default=None)

    def is_authorized(self):
        return (self.oauth_token and self.oauth_token_secret or
                self.oauth_verifier)

    def get_or_create(
        cls,
        app_hash,
        oauth_token=None,
        oauth_token_secret=None,
        oauth_verifier=None,
    ):
        try:
            user = cls.query.filter_by(app_hash=app_hash).one()
        except NoResultFound:
            user = cls(
                app_hash,
                oauth_token,
                oauth_token_secret,
                oauth_verifier,
            ).save()
        return user

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
