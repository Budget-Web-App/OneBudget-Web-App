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

class login_form(FlaskForm):
    email = StringField(validators=[InputRequired(), Email(), Length(1, 64)])
    password = PasswordField(validators=[InputRequired()])
    rememberme = BooleanField('Keep me logged in')
    login = SubmitField('Log In')
    _user = None

    @staticmethod
    def validate_email(form,email):
        user = User.query.filter(User.email==form.email.data).first()
        if not user:
            raise ValidationError("Unknown Email")
        form._user=user

    @staticmethod
    def validate_password(form,password):
        if form._user is None:
            raise ValidationError() #just to be sure
        if not check_password_hash(form._user.password, password.data): #passcheck embedded into user model
            raise ValidationError("Password incorrect")