from lib2to3.pgen2 import token
from flask import Flask, Blueprint, redirect, url_for, render_template, make_response, request
from requests.exceptions import HTTPError, RequestException
import requests
import logging
from signin_form import signin_form
from signup_form import signup_form
import os
import jwt

# view = Blueprint("view", __name__, template_folder='templates',
#                 static_folder='static')


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret"
    app.config["APP_NAME"] = os.environ.get("APP_NAME")
    app.config["TOKEN_NAME"] = 'token'
    app.config["SIGNIN_URI"] = 'http://{0}/signin'.format(
        os.environ.get("USERSERVICE_API_ADDR"))
    app.config["SIGNUP_URI"] = 'http://{0}/signup'.format(
        os.environ.get("USERSERVICE_API_ADDR"))
    # app.register_blueprint(view)

    # Set up logger
    app.logger.handlers = logging.getLogger('gunicorn.error').handlers
    app.logger.setLevel(logging.getLogger('gunicorn.error').level)
    app.logger.info('Starting frontend.')

    @app.route('/')
    def root():
        return redirect(url_for('signin'))

    @app.route('/signin', methods=['GET', 'POST'])
    def signin():
        form = signin_form()

        if request.method == "POST":

            if form.validate():
                username = request.form['email']
                password = request.form['password']

                successful_signin = _signin_helper(username, password)
                if successful_signin is not None:
                    return successful_signin
            return render_template("auth/signin(new).html", form=form, program_name=app.config["APP_NAME"])
        elif request.method == 'GET':
            token = request.cookies.get(app.config['TOKEN_NAME'])

            if verify_token(token):
                # already authenticated
                app.logger.debug(
                    'User already authenticated. Redirecting to /budget')
                return redirect(url_for('load_budget'))

            return render_template("auth/signin(new).html", form=form, program_name=app.config["APP_NAME"])

    @app.route('/signup', methods=['GET'])
    def signup():
        form = signup_form()
            
        if request.method == 'POST':
            if form.validate():
                try:
                    username = request.form['email']
                    password = request.form['password']
                    app.logger.debug('Signing up.')

                    resp = requests.post(url=app.config["SIGNUP_URI"], data={
                        'email': username, 'password': password, 'timezone': 'GMT-12:00'})
                    
                    if resp.status_code == 201:
                        succesful_signin = _signin_helper(username, password)

                except requests.exceptions.RequestException as err:
                    app.logger.error('Error creating new user: %s', str(err))
        
        return render_template('auth/signup.html', form=form, program_name=app.config["APP_NAME"])

    @app.route('/signout', methods=['GET'])
    def signout():
        """
        Logs out user by deleting token cookie and redirecting to login page
        """
        app.logger.info('Logging out.')
        resp = make_response(redirect(url_for('signin')))
        resp.delete_cookie(app.config['TOKEN_NAME'])
        return resp

    @app.route('/resetpassword', methods=['GET'])
    def reset_password():
        return {"data": "Good"}, 200

    @app.route('/budget', methods=['GET'])
    def load_budget():
        return {"data": "Good"}, 200

    @app.route('/privacy-policy', methods=['GET'])
    def privacy_policy():
        return {"data": "Good"}, 200

    @app.route('/terms', methods=['GET'])
    def terms():
        return {"data": "Good"}, 200

    def verify_token(token):
        if token is None:
            return False
        return True

    def _signin_helper(username, password):
        try:
            app.logger.debug('Signing in.')

            req = requests.get(url=app.config["SIGNIN_URI"], params={
                        'email': username, 'password': password})

            req.raise_for_status()  # Raise on HTTP Status code 4XX or 5XX

            # Get token from response
            token = req.json()['token'].encode('utf8')

            claims = jwt.decode(token, verify=False)

            # Set max age for token cookie
            max_age = claims['exp'] - claims['ait']

            # Generate redirect to budget add token to http only cookies
            resp = make_response(redirect(url_for('load_budget')))
            resp.set_cookie(
                        app.config["TOKEN_NAME"], token, max_age=max_age)
            return resp
        except (RequestException, HTTPError) as err:
            app.logger.error('Error logging in: %s', str(err))

    return app
