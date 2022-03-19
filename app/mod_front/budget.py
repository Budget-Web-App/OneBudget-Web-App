from unicodedata import category
from flask import render_template, Flask, url_for, request
import calendar
import requests
from datetime import datetime
from flask_modals import render_template_modal
from app.mod_front.common import view
from flask_login import current_user, login_required
import json


def init_route(app):
    @view.route("/budget")
    def budget_new():
        return render_template('/main/budget_new.html')

    @view.route("/<string:budget_id>/budget/<int:year>/<int:month>")
    @login_required
    def budget(budget_id: str, year: int, month: int):

        # Get current year
        app.config['CURRENT_YEAR'] = datetime.now().year

        # Get current Month
        app.config['CURRENT_MONTH'] = datetime.now().month

        month_short = calendar.month_abbr[month]
        month_long = calendar.month_name[month]

        url = "http://{0}{1}".format(request.host, url_for(
            'api.beta.budgets.list_budgets', user_id=current_user.id))
        budget_information_raw = requests.get(url)
        budget_information = json.loads(budget_information_raw.text)

        if budget_information["data"] == []:
            create_default()

        print(budget_information["data"][0]["budget_id"])

        category_url = "http://{0}/api/beta/budgets/{1}/categories/".format(request.host, budget_information["data"][0]["budget_id"])
        
        categories_raw = requests.get(category_url)
        categories_dict = json.loads(categories_raw.text)
        categories = categories_dict["data"]
        print(categories)

        app.config['budget_name'] = "let's get this bread 🤑"
        app.config['email_address'] = "canadyreceipts@gmail.com"

        Age_of_Money = "13"
        total_of_budget_accounts = "444.69"
        total_of_tracking_accounts = "22,963.45"
        to_be_budgeted_amount = "100.00"
        age_of_money = "12"
        amount_to_assign = "64.48"

        # Calculating next year
        next_year = year+1 if month == 12 else year

        # Calculating next mont
        next_month = month+1 if month != 12 else 1

        return render_template(
            '/main/budget.html',
            categories=categories,
            budget_name=app.config['budget_name'],
            email_address=current_user.email,
            program_name=app.config['program_name'],
            Age_of_Money=Age_of_Money,
            to_be_budgeted_amount=to_be_budgeted_amount,
            total_of_budget_accounts=total_of_budget_accounts,
            total_of_tracking_accounts=total_of_tracking_accounts,
            age_of_money=age_of_money,
            amount_to_assign=amount_to_assign,
            year=year,
            month=month,
            month_short=month_short,
            month_long=month_long,
            currentyear=app.config['CURRENT_YEAR'],
            currentmonth=app.config['CURRENT_MONTH'],
        )


def create_default():
    url = "http://{0}{1}".format(request.host,
                                 url_for('api.beta.budgets.list_budgets'))
    body = {
        "name": "new_budget",
        "user_id": current_user.id,
    }
    requests.post(
        url=url,
        data=body
    )
