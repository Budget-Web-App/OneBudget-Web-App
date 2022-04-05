import code
from flask import Blueprint, request, redirect, url_for, flash, jsonify,render_template
from beta import routes

beta_blueprint = Blueprint('beta', __name__, url_prefix="/beta")

def register_version(app):
    routes.register_routes(app, beta_blueprint)
    app.register_blueprint(beta_blueprint)
    