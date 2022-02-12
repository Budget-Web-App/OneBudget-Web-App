from flask import render_template
from . import accounts, budget
from .reports import spendingTotals, networth, incomeExpense


def init_app(app):
    accounts.init_route(app)
    budget.init_route(app)
    spendingTotals.init_route(app)
    networth.init_route(app)
    incomeExpense.init_route(app)
