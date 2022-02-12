from importlib.resources import Resource
import flask
from flask_restful import Resource,Api

api_bp = flask.Blueprint('beta', __name__)
custom_api = Api(api_bp)

class Budgets(Resource):
    def list():
        return jsonify({"data":"Budgets list"})
    def get(budgetId:str):
        return jsonify({"data":"budget info"})

custom_api.add_resource(Budgets,'/api/beta/budgets')
custom_api.add_resource(Budgets,'/api/beta/budgets/<string:budgetId>')