from flask import Blueprint, request, g
from app.mod_db.models import User


# Blueprint to Append /beta as url prefix
categories_blueprint = Blueprint(
    'categories', __name__, url_prefix="/budgets/<budget_id>/categories")


def register_route(parent):
    parent.register_blueprint(categories_blueprint)

    @categories_blueprint.url_defaults
    def add_language_code(endpoint, values):
        values.setdefault('budget_id', g.budget_id)

    @categories_blueprint.url_value_preprocessor
    def pull_budget_id(endpoint, values):
        g.budget_id = values.pop('budget_id')

    @categories_blueprint.route("/", methods=["GET", "POST"])
    def list_categories():
        """
        """
        # if request.method == "POST":
        return {"data": {"budget_id":g.budget_id}}

    @categories_blueprint.route("/<string:user_id>", methods=["GET", "PUT", "DELETE"])
    def category(user_id):
        """
        """
        return {"data": {}}
