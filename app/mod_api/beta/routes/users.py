from flask import Blueprint, request


# Blueprint to Append /beta as url prefix
users = Blueprint('users', __name__, url_prefix="/users")

def register_route(parent):
    parent.register_blueprint(users)
    @users.route("/", methods=["GET", "POST"])
    def list_users():
        """
        """
        #if request.method == "POST":
        return {"data": {}}
    
    @users.route("/<string:user_id>",methods=["GET","PUT","DELETE"])
    def user(user_id):
        """
        """
        return {"data": {}}