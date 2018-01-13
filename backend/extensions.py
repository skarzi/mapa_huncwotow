from flask_cors import CORS
from flask_restful import Api
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

restful_api = Api(catch_all_404s=True)
db = SQLAlchemy()
cors = CORS()
_session = Session()
