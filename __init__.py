import routes
from flask import Flask


def create_app():
    app = Flask(__name__)
    # models.init_app(app)
    routes.init_app(app)
    # services.init_app(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(use_reloader=True, debug=True)
