import app
from flask_modals import Modal

if __name__ == "__main__":
    application = app.create_app()
    
    application.config['program_name'] = "1Budget"
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # load modals


    # run app
    application.run(use_reloader=True, debug=True,host="192.168.1.212")
