from flask import jsonify, render_template
import calendar
from datetime import datetime


def init_route(app):
    @app.route("/accounts")
    def accounts():
        app.config['budget_name'] = "let's get this bread 🤑"
        app.config['email_address'] = "canadyreceipts@gmail.com"
        # Get current year
        app.config['CURRENT_YEAR'] = datetime.now().year

        # Get current Month
        app.config['CURRENT_MONTH'] = datetime.now().month

        return render_template(
            '/main/accounts.html',
            budget_name=app.config['budget_name'],
            email_address=app.config['email_address'],
            program_name=app.config['program_name'],
            currentyear=app.config['CURRENT_YEAR'],
            currentmonth=app.config['CURRENT_MONTH']
        )
