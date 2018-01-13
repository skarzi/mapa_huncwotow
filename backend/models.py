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
        return bool(self.oauth_token) and bool(
            self.oauth_token_secret) and bool(self.oauth_verifier)

    @classmethod
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
                app_hash=app_hash,
                oauth_token=oauth_token,
                oauth_token_secret=oauth_token_secret,
                oauth_verifier=oauth_verifier,
            ).save()
        return user

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self
