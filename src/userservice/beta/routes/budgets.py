from distutils.log import error
from flask import Blueprint, request, jsonify
#from app.mod_db import db
from src.userservice.beta.routes import categories
from app.mod_db.models.users import Budget

# Blueprint to Append /beta as url prefix
budgets_blueprint = Blueprint('budgets', __name__, url_prefix="/budgets")


def register_route(parent):
    parent.register_blueprint(budgets_blueprint)

    @budgets_blueprint.route("/", methods=["GET", "POST"])
    def list_budgets():
        """
        """
        if request.method == "POST":
            budget_name = request.form.get('name')
            budget_notes = request.form.get('notes')
            user_id = request.form.get('user_id')
            new_budget = Budget(
                budget_name=budget_name,
                budget_notes=budget_notes,
                budget_user_id=user_id,
            )
            db.session.add(new_budget)
            db.session.commit()
            return {"data": new_budget.to_dict(show_all=True)}
        elif request.method == "GET":
            user_id = request.args.get("user_id")

            if user_id:
                budgets = Budget.query.filter_by(budget_user_id=user_id).all()
            else:
                budgets = Budget.query.all()

            if not budgets:
                return jsonify(data=[]), 404
            return jsonify(data=[budget.to_dict(show_all=True) for budget in budgets])
