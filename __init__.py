import app

if __name__ == "__main__":
    application = app.create_app()
    # run app
    application.run(use_reloader=True, debug=True)
