""" Top level module
This module:
- Contains create_app()
- Registers extensions
"""

import sys
from apps.predict_booking.blueprints import predictbooking_bp
from extensions import bcrypt, cors, db, jwt, ma
from flask import Flask


def create_app(config_name):
    """Creates a flask app"""
    app_banner = """
    **************************************************
    *                                                *
    *          Welcome to Flask App                  *
    *                                                *
    **************************************************
    """
    app = Flask(__name__)
    cli = sys.modules["flask.cli"]
    # cli.show_server_banner = lambda *x: None
    cli.show_server_banner = lambda *x: print(app_banner)

    register_extensions(app)

    # Register blueprints
    app.register_blueprint(predictbooking_bp, url_prefix="/api/predictbooking/")

    return app


def register_extensions(app):
    """Registers flask extensions"""
    # db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
