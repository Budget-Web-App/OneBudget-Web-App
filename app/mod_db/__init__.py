from flask_sqlalchemy import SQLAlchemy


def init_db(app):
    # adding configuration for using a sqlite database
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{0}:{1}@{2}/mySchema".format(
        "root", "secret", "127.0.0.1:3306")
    # Creating an SQLAlchemy instance
    return SQLAlchemy(app)
