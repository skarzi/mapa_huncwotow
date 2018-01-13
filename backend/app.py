import importlib

from flask import Flask

from .extensions import (
    cors,
    db,
    restful_api,
    _session,
)


def create_app(config_name=None, init_extensions=True):
    importlib.import_module('backend.resources')
    app = Flask(__name__)
    app.config.from_object('backend.settings')
    if init_extensions:
        db.init_app(app)
        restful_api.init_app(app)
        cors.init_app(app)
        _session.init_app(app)
    return app
