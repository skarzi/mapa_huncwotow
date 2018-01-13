from flask_restful import Resource

from ..extensions import restful_api


@restful_api.resource('/ping')
class Ping(Resource):
    def get(self):
        return {'message': 'pong'}
