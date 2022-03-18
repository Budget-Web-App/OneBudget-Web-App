from flask import Blueprint, request


# Blueprint to Append /beta as url prefix
users = Blueprint('users', __name__, url_prefix="/users")

def register_route():
    @users.route("/", methods=["GET", "POST"])
    def users():
        """
        """
        #if request.method == "POST":
    
    @users.route("/<string:user_id>",methods=["GET","PUT","DELETE"])
    def user(user_id):
        """
        """
    