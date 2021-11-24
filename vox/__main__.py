import sys


from vox.downloader import YTDLDownloader
from vox.session import BasicSession

##
# def init():
#     # write to a log file indicating the that the application is running #
#     while 1:
#         time.sleep(5)
#         print("application running...")
#         run_flask_server()
#         # # create log file and write
#         # with open("log.txt", "a") as myfile:
#         #     now = datetime.now()
#         #     time_now = now.strftime("%H:%M:%S")
#         #     myfile.write("log application running..." + str(time_now) + "\n")
##

if __name__ == "__main__":

    # run the session, passing in the  #
    # from vox.data_entry import db
    # from flask import Flask

    # app = Flask("something")
    # # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vox.db"
    # app.register_blueprint(reporting)
    # db.init_app(app)

    # with app.app_context():
    #     db.create_all()

    start_session = BasicSession()
    start_session.run_session()

    # just tread water on this thread #
