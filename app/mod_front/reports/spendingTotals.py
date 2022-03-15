from flask import render_template
from datetime import datetime
import requests
from app.mod_front.reports.common import reports


def init_route(app):
    @reports.route("/<string:budget_id>/spending/totals")
    def spendingTotals(budget_id: str):
        # Get current year
        currentyear = datetime.now().year
        # Get current Month
        currentmonth = datetime.now().month
        budget_name = "let's get this bread 🤑"
        email_address = "canadyreceipts@gmail.com"

        categories = get_categories(budget_id)

        total_spending = sum([float(categories[i]["spending"])
                             for i in range(len(categories))])

        return render_template('/reports/spendingTotals.html',
                               budget_name=budget_name,
                               email_address=email_address,
                               len=len(categories),
                               categories=categories,
                               total_spending=total_spending,
                               currentyear=currentyear,
                               currentmonth=currentmonth
                               )


def get_categories(budget_id: str) -> list:
    URI = "http://127.0.0.1:5000/api/beta/budgets/{0}".format(budget_id)
    response = requests.get(URI)
    # Checks for errors
    response.raise_for_status()
    return response.json()["data"]
