from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.mod_db import db
from app.mod_db.models import User
from app.forms.signin_form import login_form
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms.signin_form import login_form

auth = Blueprint("auth", __name__, url_prefix="/")


def init_route(app):
    @auth.route("/login", methods=["GET", "POST"])
    def login():
        form = login_form()
        if form.validate_on_submit():
            login_user(form._user,remember=form.rememberme.data)
            print("Here")
            return redirect(url_for('view.budget_new'))
        return render_template('auth/signin.html', title='Sign In', form=form)

    @auth.route('/signup', methods=['GET'])
    def sign_up():

        return render_template("/auth/signup.html")

    @auth.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("views.home"))
    
    app.register_blueprint(auth)
