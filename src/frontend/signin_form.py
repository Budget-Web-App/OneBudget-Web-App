from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    DateField,
    TextAreaField,
    SubmitField,
)
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Length, EqualTo, Email, Regexp ,Optional, ValidationError
import email_validator
from werkzeug.security import generate_password_hash, check_password_hash

class signin_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    password = PasswordField(validators=[InputRequired()])
    rememberme = BooleanField('Keep me logged in')
    signin = SubmitField('Sign In')
    _user = None