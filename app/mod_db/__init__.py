from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def init_db(app):
    # adding configuration for using a sqlite database
    #app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{0}:{1}@{2}/mySchema".format(
    #    "root", "secret", "127.0.0.1:3306")

    db.init_app(app)

    if not path.exists("website/" + DB_NAME):
        # Only good for testing, to be changed later
        db.create_all(app=app)
