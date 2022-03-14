from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.mod_db import db
from app.mod_db.models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__, url_prefix="/")


def init_route(app):

    @auth.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")

            user = User.query.filter_by(email=email).first()

            if user:
                if check_password_hash(user.password, password):
                    flash("logged in!", category='success')
                    return redirect(url_for('mod_front.budget'))
                else:
                    flash('Password is incorrect!', category='error')
            else:
                flash('User does not exist', category='error')

        email = request.form.get("email")
        password = request.form.get("password")
        return render_template("/auth/signin.html")

    @auth.route('/signup', methods=['GET', 'POST'])
    def sign_up():

        if request.method == 'POST':
            email = request.form.get('email')
            username = request.form.get('username')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')

            email_exists = User.query.filter_by(email=email).first()
            username_exists = User.query.filter_by(username=username).first()

            if email_exists:
                flash('Email is already in use.', category='error')
            elif username_exists:
                flash('Username is already in use.', category='error')
            elif password1 != password2:
                flash('Passwords don\'t match!', category='error')
            elif len(username) < 2:
                flash('Username is too short.', category='error')
            elif len(password1) < 6:
                flash('Password is too short', category='error')
            else:
                password_hash = generate_password_hash(
                    password=password1, method='sha256')

                new_user = User(email=email, username=username,
                                password=password_hash)
                db.session.add(new_user)
                db.session.commit()

                login_user(new_user, remember=True)

                flash('User Created!')
                return redirect(url_for('mod_front.accounts'))

        return render_template("/auth/signup.html")

    @auth.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("views.home"))
    
    app.register_blueprint(auth)
