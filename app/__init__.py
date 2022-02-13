from flask import Flask
from app import mod_front, mod_api, mod_db


def create_app():
    app = Flask(__name__)
    # models.init_app(app)
    mod_front.init_app(app)
    mod_api.init_api(app)
    app.register_blueprint(mod_api.api_bp)
    # services.init_app(app)
    return app
