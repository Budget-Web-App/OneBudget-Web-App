from unicodedata import category
from flask import render_template,jsonify,make_response
import calendar
from datetime import datetime


def init_route(app):
    @app.route("/<string:budget_id>/budget/<int:year>/<int:month>")
    def budget(budget_id:str, year: int, month: int):
        # Get current year
        currentyear=datetime.now().year
        # Get current Month
        currentmonth=datetime.now().month
        month_short = calendar.month_abbr[month]
        month_long = calendar.month_name[month]
        budget_name = "let's get this bread 🤑"
        email_address = "canadyreceipts@gmail.com"
        program_name = "1Budget"
        Age_of_Money = "13"
        total_of_budget_accounts = "444.69"
        total_of_tracking_accounts = "22,963.45"
        to_be_budgeted_amount = "100.00"
        age_of_money = "12"
        amount_to_assign = "64.48"

        #Calculating next year
        next_year = year+1 if month==12 else year
        #Calculating next mont
        next_month = month+1 if month!=12 else 1

        return render_template(
            '/main/budget.html',
            budget_name=budget_name,
            email_address=email_address,
            program_name=program_name,
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
            currentyear=currentyear,
            currentmonth=currentmonth
        )
    @app.route("/api/beta/budget/<string:budget_id>")
    def get(budget_id:str):
        if(budget_id == "1"):
            categories = [
            {
                "color": "rgb(205, 234, 159)",
                "name": "Household Spending 💵",
                "spending": "6343.06"
            },
            {
                "color": "rgb(176, 135, 196)",
                "name": "Monthly Transactions 📅",
                "spending": "3866.00"
            },
            {
                "color": "rgb(154, 208, 93)",
                "name": "Personal Spending 💵",
                "spending": "2164.98"
            },

            {
                "color": "rgb(90, 179, 234)",
                "name": "Adulting",
                "spending": "2006.68"
            },

            {
                "color": "rgb(226, 97, 54)",
                "name": "Debt 💸",
                "spending": "1713.33"
            },

            {
                "color": "rgb(255, 234, 169)",
                "name": "Pets 🐾",
                "spending": "576.80"
            },

            {
                "color": "rgb(223, 210, 229)",
                "name": "Giving 🤲🏻",
                "spending": "522.83"
            },

            {
                "color": "rgb(253, 203, 85)",
                "name": "Yearly Transactions 📅",
                "spending": "502.66"
            },

            {
                "color": "rgb(244, 158, 139)",
                "name": "Savings 💰",
                "spending": "500.00"
            },

            {
                "color": "rgb(216, 233, 247)",
                "name": "Gift Cards & Cash",
                "spending": "275.03"
            }
        ]
            return make_response(jsonify({"data":categories}),200)