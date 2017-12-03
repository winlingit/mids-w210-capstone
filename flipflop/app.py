from flask import Flask

from lib.populate_database import populate

from flipflop.blueprints.page import page
from flipflop.blueprints.api import api
from flipflop.blueprints.find import find
from flipflop.blueprints.track import track

from flipflop.extensions import (
    debug_toolbar,
    db
)


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    #app.config.from_pyfile('settings.py', silent=True)

    if settings_override:
        app.config.update(settings_override)

    app.register_blueprint(page)
    app.register_blueprint(api)
    app.register_blueprint(find)
    app.register_blueprint(track)
    extensions(app)

    populate(app)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    debug_toolbar.init_app(app)
    db.init_app(app)

    return None
