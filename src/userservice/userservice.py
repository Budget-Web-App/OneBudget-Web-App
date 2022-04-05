from curses import raw
from flask import Flask, request, jsonify
from db import UserDb, BudgetDb, CategoryDb
import sys
from sqlalchemy.exc import OperationalError, SQLAlchemyError
import os
import logging
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt
from datetime import datetime, timedelta
import jwt
import bleach
import sqlalchemy
import re
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

class TokenError(Exception):
    pass

class ArgumentError(Exception):
    pass


def create_app():
    """Flask application factory to create instances
    of the Userservice Flask App
    """
    app = Flask(__name__)

    # Register Beta version of the API
    # beta.register_version(app)

    def requires_token(func):
        """Used to check if the path has a token

        Args:
            func (function): _description_
        """
        def _requires_token(*args, **kwargs):
            try:
                raw_token = request.headers.get(app.config['TOKEN_NAME'])

                if raw_token is None:
                    raise TokenError("No token provided")

                # Encodes token for verification
                token = raw_token.encode('utf8')

                if not verify_token(token):
                    raise UserWarning("user is not authenticated")

                func(*args, **kwargs)
            except UserWarning as e:
                app.logger.error("Error validating token: %s", str(e))
                return str(e), 401

        return _requires_token

    @app.route("/signin", methods=["Get"])
    def signin():
        app.logger.debug('Sanitizing login input.')
        try:
            raw_email = request.args.get('email')

            if raw_email is None:
                raise ValueError("No email argument provided")

            raw_password = request.args.get('password')

            if raw_password is None:
                raise ValueError("No password argument provided")

            remember_me = request.form.get('rememberme', False, bool)

            email = bleach.clean(raw_email)
            password = bleach.clean(raw_password)

            user = users_db.get_user(email)
            if user is None:
                raise LookupError('user {0} does not exist'.format(email))

            # Validate the password
            if not bcrypt.checkpw(password.encode('utf-8'), user["passhash"]):
                raise PermissionError('Invalid login')

            # Generates token
            token = __generate_new_token(user)

            return jsonify({'token': token.decode("utf-8")}), 200

        except LookupError as err:
            return str(err), 404
        except PermissionError as err:
            return str(err), 401
        except ValueError as err:
            return str(err), 400

    @app.route("/signup", methods=["POST"])
    def signup():
        try:
            app.logger.debug('Sanitizing input.')
            req = {k: bleach.clean(v) for k, v in request.form.items()}
            __validate_new_user(req)

            if users_db.get_user(req["email"]) is not None:
                raise LookupError(
                    "email {0} is already in use".format(req["email"]))

            accountid = users_db.generate_userid()

            app.logger.debug('generating password hash')
            password = req["password"]
            salt = bcrypt.gensalt()
            passhash = bcrypt.hashpw(password.encode('utf-8'), salt)
            app.logger.info('Successfully generated password hash')

            user_data = {
                "userid": accountid,
                "email": req["email"],
                "timezone": req["timezone"],
                "passhash": passhash
            }

            # Add user_data to database
            app.logger.debug("Adding user to the database")
            users_db.add_user(user_data)
            app.logger.info("Successfully created user.")

            user = users_db.get_user(user_data["email"])
            del user["passhash"]

            return jsonify(user), 201
        except UserWarning as warn:
            app.logger.error("Error creating new user: %s", str(warn))
            return str(warn), 400
        except NameError as err:
            app.logger.error("Error creating new user: %s", str(err))
            return str(err), 409
        except SQLAlchemyError as err:
            app.logger.error("Error creating new user: %s", str(err))
            return 'failed to create user', 500
        except Exception as e:
            return str(e), 404

    @app.route("/<user_id>/budgets", methods=["POST"])
    @requires_token
    def add_users_budgets(user_id: str):
        try:
            allowed_args = []

            all_provided_args = request.args.listvalues()

            #__validate_provided_args(all_provided_args, allowed_args)

            # get display name from form
            raw_displayname = request.form.get('displayname', None, str)
            # get budget notes from form
            raw_budgetnotes = request.form.get('notes', "", str)

            if raw_displayname is None:
                raise ValueError("No display name argument provided")

            budgetid = budgets_db.generate_budgetid()
            budgetnotes = bleach.clean(raw_budgetnotes)
            displayname = bleach.clean(raw_displayname)

            #auth_payload = get_token_data(request.headers.get(app.config['TOKEN_NAME']).encode('utf8'))

            #if user_id != auth_payload["userid"]:
            #    raise PermissionError

            budget_data = {
                "budgetid": budgetid,
                "displayname": displayname,
                "budgetnotes": budgetnotes,
                "accessdate": datetime.utcnow(),
                "userid": user_id,
            }

            # Add user_data to database
            app.logger.debug("Adding budget to the database")
            budgets_db.add_budget(budget_data)
            app.logger.info("Successfully created budget.")

            budget = budgets_db.get_budget(budget_data["budgetid"])

            return jsonify(budget), 201
        except ArgumentError as e:
            app.logger.error("Error creating budget: %s", str(e))
            return str(e), 401

        except UserWarning as e:
            app.logger.error("Error validating token: %s", str(e))
            return str(e), 401
        
        except TokenError as e:
            app.logger.error("Error validating token: %s", str(e))
            return str(e), 404

        except ValueError as e:
            app.logger.error("Error creating budget: %s", str(e))
            return str(e), 401

        except Exception as e:
            app.logger.error("Unknown error creating budget: %s", str(e))
            return str(e), 500

    @app.route("/<user_id>/budgets", methods=["GET"])
    def get_users_budgets(user_id: str):

        try:
            # Get all budgets that belong to this user
            app.logger.debug("fetching budgets of %s", user_id)
            budgets = budgets_db.get_budgets(user_id)
            app.logger.debug("successfully got budgets")

            return jsonify({"values": budgets}), 201

        except SQLAlchemyError as err:
            app.logger.error("Error fetching budgets: %s", str(err))
            return 'failed to fetch budgets', 500

    @app.route("/<user_id>/budgets/<budget_id>", methods=["GET"])
    def get_users_budget(user_id: str, budget_id: str):
        try:
            # Get all budget with the specified id
            app.logger.debug("fetching budget with id of %s", budget_id)
            budget = budgets_db.get_budget(budget_id)
            app.logger.debug("successfully got budget")

            app.logger.debug("fetching budget categories")
            categories = categories_db.get_categories(budget_id)
            app.logger.debug("successfully got categories")

            budget["categories"] = categories

            return jsonify(budget), 201

        except SQLAlchemyError as err:
            app.logger.error("Error fetching budgets: %s", str(err))
            return 'failed to fetch budgets', 500

    @app.route("/<user_id>/budgets/<budget_id>", methods=["PATCH"])
    def update_users_budget(user_id: str, budget_id: str):

        try:

            req = {k: bleach.clean(v) for k, v in request.form.items()}
            req["budgetid"] = budget_id
            req["accessdate"] = datetime.utcnow()

            if budgets_db.get_budget(req["budgetid"]) is None:
                raise LookupError(
                    "budget with id {0} not found".format(req["budgetid"]))

            app.logger.debug("Updating budget with id %s", req["budgetid"])
            budgets_db.update_budget(req)
            app.logger.debug("Successfully updated budget")

            budget = budgets_db.get_budget(req["budgetid"])

            return jsonify(budget), 201

        except LookupError as err:
            app.logger.error("Error updating budget: %s", str(err))
            return str(err), 404

        except SQLAlchemyError as err:
            app.logger.error("Error creating new user: %s", str(err))
            return 'failed to update budget', 500

    @app.route("/<user_id>/budgets/<budget_id>", methods=["DELETE"])
    def remove_users_budget(user_id: str, budget_id: str):
        try:

            if budgets_db.get_budget(budget_id) is None:
                raise LookupError(
                    "budget with id {0} not found".format(budget_id))

            app.logger.debug("Deleting budget with id %s", budget_id)
            budgets_db.delete_budget(budget_id)
            app.logger.debug("Successfully deleted budget")

            budget = budgets_db.get_budget(budget_id)

            return jsonify({}), 201

        except LookupError as err:
            app.logger.error("Error deleting budget: %s", str(err))
            return str(err), 404

        except SQLAlchemyError as err:
            app.logger.error("Error creating new user: %s", str(err))
            return 'failed to delete budget', 500

    @app.route('/<user_id>/budgets/<budget_id>/categories', methods=["POST"])
    def add_budget_category(user_id: str, budget_id: str):
        try:

            #token = request.cookies.get(app.config['TOKEN_NAME'])
            # if not verify_token(token):
            #    raise UserWarning("user is not authenticated")

            #auth_payload = get_token_date()

            raw_displayname = request.args.get('displayname', None, str)

            if raw_displayname is None:
                raise ValueError("No display name argument provided")

            raw_parentid = request.args.get('parentid', None, str)

            categoryid = categories_db.generate_categoryid()
            displayname = bleach.clean(raw_displayname)

            parentid = bleach.clean(
                raw_parentid) if raw_parentid is not None else None

            if (parentid is not None) and (categories_db.get_category(parentid) is None):
                raise LookupError(
                    "Unable to find category with Id %s", parentid)

            # if user_id != auth_payload["userid"]:
            #    raise PermissionError

            category_data = {
                "categoryid": categoryid,
                "displayname": displayname,
                "parentid": parentid,
                "budgetid": budget_id,
            }

            # Add user_data to database
            app.logger.debug("Adding category to the database")
            categories_db.add_category(category_data)
            app.logger.info("Successfully created category.")

            budget = categories_db.get_category(category_data["categoryid"])

            return jsonify(budget), 201
        except LookupError as e:
            app.logger.error("Error creating category: %s", str(e))
            return str(e), 401

        except UserWarning as e:
            app.logger.error("Error validating token: %s", str(e))
            return str(e), 401

        except ValueError as e:
            app.logger.error("Error creating category: %s", str(e))
            return str(e), 401

        except SQLAlchemyError as err:
            app.logger.error("Error creating new category: %s", str(err))
            return 'failed to create category', 500

    def verify_token(token):
        """
        Validates token using userservice public key
        """
        app.logger.debug('Verifying token.')
        if token is None:
            return False
        try:
            jwt.decode(token, key=get_private_key(),
                       algorithms='RS256', verify=False)
            app.logger.debug('Token verified.')
            return True
        except jwt.exceptions.InvalidTokenError as err:
            app.logger.error('Error validating token: %s', str(err))
            return False

    def get_token_data(token):
        app.logger.debug('Getting token data.')
        if token is None:
            return None
        try:
            token = jwt.decode(token, key=get_private_key(),
                               algorithms='RS256', verify=False)
            return token
        except jwt.exceptions.InvalidTokenError as err:
            app.logger.error('Error getting token: %s', str(err))
            return None

    def get_public_key():
        public_rsakey = load_pem_public_key(
            app.config['PUBLIC_KEY'], backend=default_backend())
        return public_rsakey

    def get_private_key():
        priv_rsakey = load_pem_private_key(
            app.config['PRIVATE_KEY'], password=app.config['SECRET'], backend=default_backend())
        return priv_rsakey

    def __validate_new_user(req):
        app.logger.debug('validating create user request: %s', str(req))
        # Check if required fields are filled
        fields = (
            'email',
            'password',
        )
        if any(f not in list(req.keys()) for f in fields):
            raise UserWarning('missing required field(s)')
        if any(not bool(req[f] or req[f].strip()) for f in fields):
            raise UserWarning('missing value for input field(s)')

        # Verify username contains only 2-15 alphanumeric or underscore characters
        # if not re.match(r"\A[a-zA-Z0-9_]{2,15}\Z", req['username']):
            #raise UserWarning('username must contain 2-15 alphanumeric characters or underscores')

    def __validate_provided_args(provide_args: dict, accepted_args: list):
        if any(arg not in accepted_args for arg in list(provide_args.keys())):
            raise ArgumentError('Unaccepted argument(s) for provided')

    def __generate_new_token(user: dict) -> bytes:
        exp_time = datetime.utcnow() + \
            timedelta(seconds=app.config['EXPIRY_SECONDS'])
        payload = {
            'email': user["email"],
            'userid': user['userid'],
            'iat': datetime.utcnow(),
            'exp': exp_time,
        }

        # Generate token
        return jwt.encode(payload, get_private_key(), algorithm='RS256')

    # Set up logger
    app.logger.handlers = logging.getLogger('gunicorn.error').handlers
    app.logger.setLevel(logging.getLogger('gunicorn.error').level)
    app.logger.info('Starting userservice.')

    #app.config['VERSION'] = os.environ.get('VERSION')
    app.config['EXPIRY_SECONDS'] = int(os.environ.get('TOKEN_EXPIRY_SECONDS'))
    app.config['PRIVATE_KEY'] = open(
        os.environ.get('PRIV_KEY_PATH'), 'rb').read()
    app.config['PUBLIC_KEY'] = open(
        os.environ.get('PUB_KEY_PATH'), 'rb').read()
    app.config['SECRET'] = bytes(os.environ.get('SECRET'), 'utf-8')
    #app.config['PUBLIC_KEY'] = open(os.environ.get('PUB_KEY_PATH'), 'r').read()

    app.config['TOKEN_NAME'] = 'token'

    # Configure database connection
    try:
        # os.environ.get("ACCOUNTS_DB_URI")
        users_db = UserDb(os.environ.get("ACCOUNTS_DB_URI"), app.logger)
        budgets_db = BudgetDb(os.environ.get("BUDGETS_DB_URI"), app.logger)
        categories_db = CategoryDb(
            os.environ.get("CATEGORIES_DB_URI"), app.logger)
    except OperationalError:
        app.logger.critical("users_db database connection failed")
        sys.exit(1)
    return app


if __name__ == "__main__":
    # Create an instance of flask server when called directly
    USERSERVICE = create_app()
    USERSERVICE.run(debug=True, use_reloader=True)
