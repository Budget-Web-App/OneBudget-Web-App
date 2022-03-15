from flask import Blueprint, request
from app import mod_db

beta = Blueprint('beta', __name__, url_prefix="/beta")


def register_route(app):
    @beta.route("/signin", methods=["GET", "POST"])
    def signin():
        if request.method == "POST":
            request_date = request.form.get('request_data')
            print(request_date)
        print('off')

def init_api_beta(app):
    register_route(app)
    #global db
    db = mod_db.init_db(app)