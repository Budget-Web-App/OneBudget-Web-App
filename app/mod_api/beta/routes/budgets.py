from flask import Blueprint, request
from app.mod_api.beta.routes import categories

# Blueprint to Append /beta as url prefix
budgets = Blueprint('budgets', __name__, url_prefix="/budgets")

def register_route():
    @budgets.route("/", methods=["GET", "POST"])
    def budgets():
        """
        """
        #if request.method == "POST":
    
    @budgets.route("/<string:user_id>",methods=["GET","PUT","DELETE"])
    def budget(user_id):
        """
        """

    