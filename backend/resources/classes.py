from flask import request
from flask_restful import Resource

from backend.extensions import restful_api
from backend.models import Users


@restful_api.resource('/classes')
class Classes(Resource):
    def get(self):
        app_hash = request.args['hash']
        user = Users.get_or_create(app_hash=app_hash)
        response = user.get_classes()
        first_classes = response[0]
        date, time = first_classes["start_time"].split()
        time = time[:-3]
        return {
            "name": first_classes["name"]["pl"],
            "room": first_classes["room_number"],
            "time": time
        }

