from .posts import posts_bp
from .users import user_bp
from .base import db


def init_app(app):
    db.init_app(app)


# project/routes/__init__.py
# ...


def init_app(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(posts_bp)
