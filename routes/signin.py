from flask import render_template


def init_app(app):
    @app.route("/signin")
    def signin():
        return render_template('./template/auth/signin.html')
