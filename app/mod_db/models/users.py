from app.mod_db import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())


class Budget(db.Model):
    __tablename__ = 'budget'
    budget_id = db.Column(db.Integer, primary_key=True)
    budget_name = db.Column(db.String(150))
    budget_notes = db.Column(db.String(150))
    #budget_currency_id = db.Column(db.Integer, db.ForeignKey())
    #budget_number_format_id = db.Column(db.Integer, db.ForeignKey)
    #budget_currency_placement_id = db.Column(db.Integer, db.ForeignKey)
    budget_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

