from importlib.resources import Resource
from sys import prefix
from flask import Blueprint, jsonify, make_response
from flask_restful import Resource, Api
from optimus_ids import Optimus
from flask_sqlalchemy import SQLAlchemy
from app import mod_db
import json
import sys
import os


api_bp = Blueprint('beta', __name__, url_prefix="/beta")
api = Api(api_bp)

my_optimus = Optimus(
    prime=1
)


def ToDict(results) -> list:
    dictList = []
    for row in results:
        row = dict(row)
        row["idbudgets"] = my_optimus.encode(row["idbudgets"])
        dictList.append(row)
    return dictList


class Colors():

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def decode(self):
        return '{:02x}{:02x}{:02x}'.format(self.red, self.green, self.blue)


def encode_emoji(encoded_emoji):
    return encoded_emoji.encode('unicode-escape')


class Budget(Resource):

    def get(self, budgetId: str):
        # Will be replaced with SQL query
        budgetID = int(budgetId)
        decodedId = my_optimus.decode(budgetId)
        query = 'SELECT * FROM Categories Where BudgetId = {0};'.format(
            decodedId)
        result = db.engine.execute(query)
        categories = ToDict(result.fetchall())
        return make_response(jsonify({"data": decodedId}), 200)


class Budgets(Resource):
    def get(self):

        try:
            result = db.engine.execute('SELECT * FROM budgets;')
            Budgets = ToDict(result.fetchall())
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            return {"message": "{0}".format(e)}

        return make_response(jsonify({"data": Budgets}), 200)


def init_api(app):
    global db
    db = mod_db.init_db(app)
    api.add_resource(Budgets, '/budgets', methods=['GET', 'POST'])
    api.add_resource(Budget, '/budgets/<int:budgetId>',
                     methods=['GET', 'PATCH', 'DELETE'])
    return api_bp
