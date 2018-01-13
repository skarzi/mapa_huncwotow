import importlib

from flask import Flask

from .extensions import (
    db,
    restful_api,
)


def create_app(config_name=None, init_extensions=True):
    importlib.import_module('backend.resources')
    app = Flask(__name__)
    app.config.from_object('backend.settings')
    if init_extensions:
        db.init_app(app)
        restful_api.init_app(app)
    return app
