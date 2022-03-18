from flask import Blueprint, request
from app.mod_db.models import User


# Blueprint to Append /beta as url prefix
categories = Blueprint('categories', __name__, url_prefix="/budgets/<budget_id>/categories")

def register_route():
    @categories.url_defaults
    def add_user_url_slug(endpoint, values):
        values.setdefault('user_url_slug', g.user_url_slug)

    @categories.url_value_preprocessor
    def pull_user_url_slug(endpoint, values):
        g.user_url_slug = values.pop('user_url_slug')
        query = User.query.filter_by(url_slug=g.user_url_slug)
        g.profile_owner = query.first_or_404()

    def register_route(app):
        @categories.route("/", methods=["GET", "POST"])
        def categories():
            """
            """
            #if request.method == "POST":
    
        @categories.route("/<string:user_id>",methods=["GET","PUT","DELETE"])
        def category(user_id):
            """
            """
        
    