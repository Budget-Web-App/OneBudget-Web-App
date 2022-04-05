from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import UserDb
#from app.mod_db.models import User
import jwt
from datetime import datetime, timedelta

def register_route(app, parent):
    @parent.route("/signin", methods=["Get"])
    def signin():
        qtc_data = request.get_json()
        print(qtc_data)


        next_url = request.args.get("next")
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = False if request.form.get('rememberme') == None else True
        user = users_db.get_user(email)
        
        # Get user data
        try:
            if user is None:
                raise LookupError('')

            # Validate the password
            if not check_password_hash(user.password, password):
                raise PermissionError('Invalid login')

            exp_time = datetime.utcnow() + timedelta(seconds=app.config['EXPIRY_SECONDS'])
            payload = {
                'email': user.email,
                'iat': datetime.utcnow(),
                'exp': exp_time,
            }
            # Generate token
            token = jwt.encode(payload, app.config['PRIVATE_KEY'], algorithm='RS256')
            return jsonify({'token': token.decode("utf-8")}), 200

        except LookupError as err:
            return str(err), 404
        except PermissionError as err:
            return str(err), 401