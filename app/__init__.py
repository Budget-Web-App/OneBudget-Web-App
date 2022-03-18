from flask import Flask, url_for
from app import mod_front, mod_api, mod_db, mod_auth
from app.mod_db import DB_NAME, db
from flask_login import LoginManager
from app.mod_db.models.users import User


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "Helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"

    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)


    @app.route("/site-map")
    def site_map():
        links = []
        for rule in app.url_map.iter_rules():
            # Filter out rules we can't navigate to in a browser
            # and rules that require parameters
            if "GET" in rule.methods and has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))
                # links is now a list of url, endpoint tuples
        return {"map":links}

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
