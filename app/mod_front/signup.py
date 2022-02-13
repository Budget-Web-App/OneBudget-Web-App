from flask import render_template


def init_app(app):
    @app.route("/signup")
    def signup():
        return render_template('./template/auth/signup.html')
