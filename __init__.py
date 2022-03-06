import app

if __name__ == "__main__":
    application = app.create_app()
    
    application.config['program_name'] = "1Budget"

    # run app
    application.run(use_reloader=True, debug=True)
