from unicodedata import name
from flask import Blueprint, request, g, jsonify
from app.mod_db import db
from app.mod_db.models.users import Category


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
        if request.method == "POST":
            name = request.form.get("name")
            parent_id = request.form.get("parent")
            new_category = Category(
                name=name,
                parent_id=parent_id,
                budget_id=g.budget_id
            )
            db.session.add(new_category)
            db.session.commit()
            return {"data":new_category.to_dict(show_all=True)}

        categories = Category.query.filter_by(budget_id=g.budget_id).all()

        return jsonify(data=[category.to_dict(show_all=True) for category in categories])

    @categories_blueprint.route("/<string:user_id>", methods=["GET", "PUT", "DELETE"])
    def category(user_id):
        """
        """
        return {"data": {}}
