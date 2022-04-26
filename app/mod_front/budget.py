from unicodedata import category
from flask import render_template, Flask, url_for, request, redirect
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
        """location where users go after sign in/up

        Returns:
            _type_: _description_
        """
        token = request.cookies.get(app.config['TOKEN_NAME'])

        if not verify_token(token):
            #user isn't authenticated

            return redirect(url_for('auth.signin'))

        url = "http://{0}{1}".format(request.host, url_for(
            'api.beta.budgets.list_budgets', user_id=current_user.id))

        print(current_user.id)
        
        budget_information_raw = requests.get(url)
        budget_information = json.loads(budget_information_raw.text)
        print(budget_information)
        if not budget_information["data"]:
            new_budget = create_default().json()["data"]
            return redirect(url_for('view.budget',budget_id=new_budget["budget_id"]))

        

        return {"data":"budgets"}

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

        category_url = "http://{0}/api/beta/budgets/{1}/categories/?filter=(parent=None)".format(request.host, budget_information["data"][0]["budget_id"])
        
        categories_raw = requests.get(category_url)
        categories_dict = json.loads(categories_raw.text)
        parent_categories = categories_dict["data"]

        categories = []

        for parent_category in parent_categories:
            category_url = "http://{0}/api/beta/budgets/{1}/categories/?filter=(parent={2})".format(request.host, budget_information["data"][0]["budget_id"], parent_category["id"])
            categories_raw = requests.get(category_url)
            categories_dict = json.loads(categories_raw.text)
            child_categories = categories_dict["data"]
            categories.append(parent_category)
            if child_categories:
                categories.extend(child_categories)
                print(parent_category["id"])
                #print(child_categories)


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

        print(categories)

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
    default_budget = requests.post(
        url=url,
        data=body
    )
    return default_budget

def verify_token(token):
    """Validates token using [] public key

    Args:
        token (_type_): _description_
    """
    if token in None:
        return False
    try:
        jwt.decode(token,key=app.config['PUBLIC_KEY'], algorithms='RS256', verify=True)