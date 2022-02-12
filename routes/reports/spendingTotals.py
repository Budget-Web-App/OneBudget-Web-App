from flask import render_template


def init_route(app):
    @app.route("/reports/spending/totals")
    def spendingTotals():
        budget_name = "let's get this bread 🤑"
        email_address = "canadyreceipts@gmail.com"

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

        total_spending = sum([float(categories[i]["spending"])
                             for i in range(len(categories))])

        return render_template('/reports/spendingTotals.html', budget_name=budget_name, email_address=email_address, len=len(categories), categories=categories, total_spending=total_spending)
