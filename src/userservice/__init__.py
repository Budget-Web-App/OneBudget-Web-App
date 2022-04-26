from budgets import budgets_api
from categories import categories_api

from flask import Flask
from sqlalchemy.exc import OperationalError
from db import UserDb, CategoryDb, MonthDb
import logging
import sys
import os


app = Flask(__name__)
app.register_blueprint(budgets_api)
app.register_blueprint(categories_api)


# Set up logger
app.logger.handlers = logging.getLogger('gunicorn.error').handlers
app.logger.setLevel(logging.getLogger('gunicorn.error').level)
app.logger.info('Starting userservice.')

#app.config['VERSION'] = os.environ.get('VERSION')
app.config['EXPIRY_SECONDS'] = int(os.environ.get('TOKEN_EXPIRY_SECONDS'))
app.config['PRIVATE_KEY'] = open(os.environ.get('PRIV_KEY_PATH'), 'rb').read()
app.config['PUBLIC_KEY'] = open(os.environ.get('PUB_KEY_PATH'), 'rb').read()
app.config['SECRET'] = bytes(os.environ.get('SECRET'), 'utf-8')
#app.config['PUBLIC_KEY'] = open(os.environ.get('PUB_KEY_PATH'), 'r').read()

app.config['TOKEN_NAME'] = 'token'

# Configure database connection
try:
    users_db = UserDb(os.environ.get("ACCOUNTS_DB_URI"), app.logger)
    months_db = MonthDb(os.environ.get("CATEGORIES_DB_URI"), app.logger)
except OperationalError:
    app.logger.critical("users_db database connection failed")
    sys.exit(1)