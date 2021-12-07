import sys
import vox.flask_app
import time

# from gevent.pool import Pool
# import gevent
# from vox.downloader import YTDLDownloader
# def background_stuff(args):
#     while True:
#         try:
#             print(args)
#             time.sleep(1)
#         except Exception as e:
#             return e
# thread = None
# _pool = None

if __name__ == "__main__":

    # run the session, passing in the  #
    # from vox.data_entry import db
    # from flask import Flask #
    # app = Flask("something")
    # # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vox.db"
    # app.register_blueprint(reporting)
    # db.init_app(app)
    # with app.app_context():
    #     db.create_all()
    # start_session = BasicVoxSession()
    # just tread water on this thread #

    vox.flask_app.create_flask_app(False)

    # librarian_process = vox.flask_app.create_background_process()
    # foreground_process = vox.flask_app.run_app_as_process(app)
    # app.run()
    # mypool = Pool(1)
    # workers = mypool.apply_async(func=background_stuff, args=("do stuff"))
    # # gevent.spawn(vox.flask_app.librarian_process)
    # # librarian_process.start()
    # socketio.run(app)
    # librarian_process.join()
    # just run until something happens#
    # while 1:
    #     time.sleep(1)
    #     print("main thread...l")
