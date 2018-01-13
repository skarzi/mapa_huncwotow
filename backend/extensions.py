from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


restful_api = Api(catch_all_404s=True)
db = SQLAlchemy()
