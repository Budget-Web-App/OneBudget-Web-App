from flask_restful import Resource, Api
from flask import Blueprint
from app.mod_api import beta

api_bp = Blueprint('api', __name__, url_prefix="/api")


def init_api(app):
    beta_api = beta.init_api(app)
    api_bp.register_blueprint(beta_api)
