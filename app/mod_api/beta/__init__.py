import code
from flask import Blueprint, request, redirect, url_for, flash, jsonify,render_template
from app import mod_db
from app.mod_api.beta import routes
from app.mod_db.models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

beta_blueprint = Blueprint('beta', __name__, url_prefix="/beta")


def register_route():
    @beta_blueprint.route("/signin", methods=["GET", "POST"])
    def signin():
        qtc_data = request.get_json()
        print(qtc_data)

        return "tanks"

        if request.method == "POST":
            qtc_data = request.get_json()
            print(qtc_data)

            return "tanks"

            next_url = request.args.get("next")
            email = request.form.get('email')
            password = request.form.get('password')
            remember_me = False if request.form.get(
                'rememberme') == None else True

            user = User.query.filter_by(email=email).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=remember_me)
                    if next_url:
                        return redirect(next_url)
                else:
                    return {"data":"invalid username or password"}
            else:
                return {"data":"user does not exist"}
        return {"data": 1}

def init_api_beta(parent):
    register_route()
    routes.register_routes(beta_blueprint)
    parent.register_blueprint(beta_blueprint)
    #global db
    #db = mod_db.init_db(app)