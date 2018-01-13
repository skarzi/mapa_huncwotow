from flask import request
from flask_restful import Resource

from backend.extensions import restful_api
from backend.models import Users, POIs


@restful_api.resource('/pois')
class POIsResource(Resource):
    def get(self):
        return {
            "pois": [poi.serialize() for poi in POIs.query.all()]
        }

    def post(self):
        data = request.get_json()
        poi = POIs.get_or_create(**data)
        return poi.serialize()
