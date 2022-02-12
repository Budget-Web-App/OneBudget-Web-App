from flask import render_template


def init_route(app):
    @app.route("/budget")
    def budget():
        budget_name = "let's get this bread 🤑"
        email_address = "canadyreceipts@gmail.com"
        program_name = "1Budget"
        Age_of_Money = "13"
        total_of_budget_accounts = "444.69"
        total_of_tracking_accounts = "22,963.45"
        to_be_budgeted_amount = "100.00"
        age_of_money = "12"
        amount_to_assign = "64.48"
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
            amount_to_assign=amount_to_assign
        )
