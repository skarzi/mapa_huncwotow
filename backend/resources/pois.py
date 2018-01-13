from flask import request
from flask_restful import Resource

from backend.extensions import restful_api
from backend.models import Users, POIs


@restful_api.resource('/pois')
class POIsResource(Resource):
    def get(self):
        user = Users.query.filter_by(app_hash=request.args['hash']).one()
        personal_data = user.get_info()
        return {
            "personal_data": {
                "name": personal_data["first_name"] + " " + personal_data["last_name"]
            },
            "pois": [poi.serialize() for poi in POIs.query.all()]
        }

    def post(self):
        data = request.get_json()
        poi = POIs.get_or_create(**data)
        return poi.serialize()
