#from .posts import posts_bp
from .users import User


# project/routes/__init__.py
# ...


def init_app(app):
    app.register_blueprint(User)
    app.register_blueprint(posts_bp)
