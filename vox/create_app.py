# # Probably want to merge this with the flask app #
# from flask import Flask
# from flask_socketio import SocketIO
# from vox.flask_app import reporting as main_blueprint
# from vox.flask_app import central_session
# from multiprocessing import Process

# async_mode = None
# socketio = SocketIO(async_mode=async_mode)


# def create_background_process():
#     bg_process = Process(target=central_session.start_librarian_process)
#     return bg_process


# def create_flask_app(debug=False):

#     # start the initial flask application #
#     app = Flask(__name__)
#     app.debug = debug
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vox.db"

#     # get the blue print for the flask application #
#     app.register_blueprint(main_blueprint)

#     # initiate the flask-socket-io application #
#     socketio.init_app(app)

#     # add reference to the data

#     return app
