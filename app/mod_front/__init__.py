from flask import render_template
from . import accounts, budget, budgets
from .reports import spendingTotals, networth, incomeExpense
from app.mod_front.common import view


def init_app(app):
    accounts.init_route(app)
    budget.init_route(app)
    spendingTotals.init_route(app)
    networth.init_route(app)
    incomeExpense.init_route(app)
    budgets.init_route(app)
    app.register_blueprint(view)
