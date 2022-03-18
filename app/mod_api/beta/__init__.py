from flask import Blueprint, request
from flask import Blueprint, request, redirect, url_for, flash
from app import mod_db
from app.mod_api.beta import routes
from app.mod_db.models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

beta_blueprint = Blueprint('beta', __name__, url_prefix="/beta")


def register_route():
    @beta_blueprint.route("/signin", methods=["GET", "POST"])
    def signin():
        if request.method == "POST":
            email = request.form.get('email')
            password = request.form.get('password')
            remember_me = False if request.form.get(
                'rememberme') == None else True

            user = User.query.filter_by(email=email).first()

            if user:
                if check_password_hash(user.password, password):
                    flash("logged in!", category='success')
                    login_user(user, remember=remember_me)
                    return redirect(url_for('view.budget', budget_id=0, month=3, year=2022))
                else:
                    flash('Password is incorrect!', category='error')
            else:
                flash('User does not exist', category='error')
        return {"data": {}}

def init_api_beta(parent):
    register_route()
    routes.register_routes(beta_blueprint)
    parent.register_blueprint(beta_blueprint)
    #global db
    #db = mod_db.init_db(app)