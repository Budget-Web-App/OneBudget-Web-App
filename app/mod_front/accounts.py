from flask import jsonify, render_template
import flask_url_map_serializer


def init_route(app):
    @app.route("/accounts")
    def accounts():
        budget_name = "let's get this bread 🤑"
        email_address = "canadyreceipts@gmail.com"
        return render_template('/main/accounts.html', budget_name=budget_name, email_address=email_address)

    @app.route("/")
    def map():
        return(jsonify({"data": flask_url_map_serializer.dump_url_map(app.url_map)}))
