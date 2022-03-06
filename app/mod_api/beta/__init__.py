from importlib.resources import Resource
from sys import prefix
from flask import Blueprint, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from app import mod_db
import json
import sys
import os

# Blueprint to Append /beta as url prefix
api_bp = Blueprint('beta', __name__, url_prefix="/beta")
api = Api(api_bp)


def ToDict(results) -> list:
    """
    ToDict Converts recieved results into dictionary,
    and encodes id.

    :param results: the results from the fetchall() function of SQLAlchemy
    :return: returns a list of dictionary entries for each of the SQL rows
    """
    dictList = []
    for row in results:
        row = dict(row)
        row["idbudgets"] = ""
        dictList.append(row)
    return dictList


class Color():

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def to_hex(self) -> str:
        """
        to_hex converts Color object to hex value

        :return: return hex color value as string 
        """
        return '{:02x}{:02x}{:02x}'.format(self.red, self.green, self.blue)

    def to_rgb(self) -> tuple:
        """
        to_hex converts Color object to rgb value

        :return: return rgb color value as tuple 
        """
        return tuple(self.red, self.green, self.blue)

    def from_hex(Hex: str):
        value = Hex.lstrip('#')
        lv = len(value)
        values = [int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3)]
        return Color(values[0], values[1], values[2])

    def from_rgb(rbg: tuple):
        return Color(rbg[0], rbg[1], rbg[2])


def encode_emoji(encoded_emoji):
    return encoded_emoji.encode('unicode-escape')


class Budget(Resource):

    def get(self, budgetId: int):
        decodedId = ""
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
