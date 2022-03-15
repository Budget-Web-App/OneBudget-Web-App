from flask import Flask
from app import mod_front, mod_api, mod_db, mod_auth
from app.mod_db import DB_NAME, db
from flask_login import LoginManager
from app.mod_db.models.users import User


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "Helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"

    mod_db.init_db(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # models.init_app(app)
    mod_auth.init_route(app)
    mod_front.init_app(app)
    mod_api.init_api(app)

    # services.init_app(app)
    return app
