import code
from flask import Blueprint, request, redirect, url_for, flash, jsonify,render_template
from app import mod_db
from app.mod_api.beta import routes
from flask_login import login_user, logout_user, login_required, current_user

beta_blueprint = Blueprint('beta', __name__, url_prefix="/beta")

def init_api_beta(parent):
    routes.register_routes(beta_blueprint)
    parent.register_blueprint(beta_blueprint)
    #global db
    #db = mod_db.init_db(app)