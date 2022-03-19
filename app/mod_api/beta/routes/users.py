from sqlalchemy import text
from flask import Blueprint, request, jsonify, url_for
from app.mod_db.models.users import User
from app.mod_db import db
from werkzeug.security import generate_password_hash, check_password_hash

# Blueprint to Append /beta as url prefix
users = Blueprint('users', __name__, url_prefix="/users")


def register_route(parent):
    parent.register_blueprint(users)

    @users.route("/", methods=["GET", "POST"])
    def list_users():
        """
        """
        if request.method == "POST":
            email = request.form.get('email')
            password1 = request.form.get('password')

            email_exists = User.query.filter_by(email=email).first()

            if email_exists:
                return {"error": "Email is already in use"}, 409
            elif len(password1) < 6:
                return {"error": "Password is too short"}, 409
            else:
                password_hash = generate_password_hash(
                    password=password1, method='sha256')

                new_user = User(email=email,
                                password=password_hash)
                db.session.add(new_user)
                db.session.commit()
                return {"data": "Successfully created new User"}
        elif request.method == "GET":
            # list(request.args.keys())

            top = request.args.get(key="top", default=50, type=int)
            filter = request.args.get(key="filter")
            order_by_args = request.args.get(key="orderBy", default="id asc", type=str)
            page = request.args.get(key="page", default=1, type=int)

            order_by = validate_orderby(order_by_args)
            users = User.get_all_pos(
                columns_order=order_by).paginate(page, top, False)

            json_data = {
                "data": [user.to_dict(show_all=True) for user in users.items],
            }

            if(users.has_next):
                json_data["next.url"] = url_for('api.beta.users.list_users', page=users.next_num)
        
            return json_data

    @users.route("/<string:user_id>", methods=["GET", "PUT", "DELETE"])
    def get_user(user_id):
        """
        """

        user = User.query.filter_by(id=user_id).first()

        if(user == None):
            return {"data": "No user found"}, 404

        if request.method == "PUT":
            """
            """

            email = request.form.get('email')
            password = request.form.get('password')

            password_hash = generate_password_hash(
                password=password, method='sha256')

            user.email = email
            user.password = password_hash

            db.session.commit()

            return {"data": "record successfully updated"}

        elif request.method == "DELETE":
            """
            """
            db.session.delete(user)
            db.session.commit()
            return {"data": "record successfully deleted"}

        elif request.method == "GET":
            return jsonify(user.to_dict(show_all=True))


def validate_filter(filters: str) -> bool:
    """
    """

    return True


def validate_orderby(order_by) -> str:
    """
    """
    order_by_seperate = order_by.replace('"', '').split(" ")
    property = order_by_seperate[0]
    direction = order_by_seperate[1] if(
        len(order_by_seperate) >= 2) else None

    return_string = "{0} {1}".format(property, direction)

    return return_string
