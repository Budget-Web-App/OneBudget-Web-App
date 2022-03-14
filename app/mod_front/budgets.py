from unicodedata import category
from flask import render_template, Flask
import calendar
import requests
from datetime import datetime
from flask_modals import render_template_modal
from app.mod_front.common import view


def init_route(app):
    @view.route("/budgets")
    def budgets():
        return render_template(
            '/main/budgets.html',
        )
