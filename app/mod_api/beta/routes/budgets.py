from flask import Blueprint, request
from app.mod_db import db
from app.mod_api.beta.routes import categories
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
            budget_notes = request.form.get('user_id')
            new_budget = Budget(
                budget_name = budget_name,
                budget_notes = budget_notes,
            )
            db.session.add(new_budget)
            db.session.commit()
            return {"data":"Successfully created Budget"}
        budgets = Budget.query.filter_by(budget_user_id=1).all()
        return {"data": budgets}
    
    @budgets_blueprint.route("/<string:user_id>",methods=["GET","PUT","DELETE"])
    def budget(user_id):
        """
        """
        return {"data": {}}