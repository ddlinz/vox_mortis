# This file simply draws together the various different flask and other interfaces. #
from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()


def create_flask_app(debug=False):

    # #
    app = Flask(__name__)
    app.debug = debug
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vox.db"

    # get the blue print for the flask application #
    from vox.flask_app import reporting as main_blueprint

    app.register_blueprint(main_blueprint)

    # #
    socketio.init_app(app)
    return app
