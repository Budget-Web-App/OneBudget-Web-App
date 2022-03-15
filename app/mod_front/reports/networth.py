from flask import render_template
from datetime import datetime
from app.mod_front.reports.common import reports

def init_route(app):
    @reports.route("/net-worth")
    def networth():
        # Get current year
        currentyear=datetime.now().year
        # Get current Month
        currentmonth=datetime.now().month
        budget_name = "let's get this bread 🤑"
        email_address = "canadyreceipts@gmail.com"
        return render_template('/reports/networth.html',
        budget_name=budget_name,
        email_address=email_address,
        currentyear=currentyear,
        currentmonth=currentmonth
        )
