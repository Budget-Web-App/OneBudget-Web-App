from flask import render_template


def init_route(app):
    @app.route("/reports/income-expense")
    def incomeExpense():
        budget_name = "let's get this bread 🤑"
        email_address = "canadyreceipts@gmail.com"
        return render_template('/reports/incomeExpense.html', budget_name=budget_name, email_address=email_address)
