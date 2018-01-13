from flask import request
from flask_restful import Resource

from backend.extensions import restful_api
from backend.models import Users


@restful_api.resource('/classes')
class Classes(Resource):
    def get(self):
        app_hash = request.args['hash']
        user = Users.get_or_create(app_hash=app_hash)
        return user.get_classes()

