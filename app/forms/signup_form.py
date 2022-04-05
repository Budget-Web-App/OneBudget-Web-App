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
from app.mod_db.models.users import User
from werkzeug.security import generate_password_hash, check_password_hash

class signup_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    password = PasswordField(validators=[InputRequired(), Length(8, 72)])
    sign_up = SubmitField('Sign Up')
    _user = None