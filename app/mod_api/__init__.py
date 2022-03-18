from flask import Blueprint, request, redirect, url_for, flash
from app.mod_api import beta
from app.mod_db.models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


api_bp = Blueprint('api', __name__, url_prefix="/api")


def register_route(app):
    @api_bp.route("/signin", methods=["GET", "POST"])
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


def init_api(app):
    register_route(app)
    beta.init_api_beta(api_bp)
    app.register_blueprint(api_bp)
