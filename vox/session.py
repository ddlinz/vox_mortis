from __future__ import unicode_literals
from abc import ABC
from re import I
import time
from vox.archive import archiveManager
from datetime import datetime

# from youtubedl.youtube_dl import YoutubeDL
from vox.downloader import YTDLDownloader
from flask import Flask, render_template, url_for
from flask_socketio import SocketIO
from multiprocessing import Queue, Process, JoinableQueue
from vox.create_app import socketio, create_flask_app

# #
# socketio = SocketIO(app, cors_allowed_origins="*")


class GeneralSession(ABC):
    def __init__(self):
        pass


class BasicSession(GeneralSession):
    # #
    def __init__(self):

        # #
        from vox.flask_app import reporting

        print("initializing session with Flask and SQL alchemy")
        self.app = create_flask_app()

        # self.app = Flask(__name__) #
        # self.app.register_blueprint(reporting) #
        # #
        self.manager = archiveManager(self.app)
        socketio.run(self.app)

        self.terminate = False

    # run the session #
    def run_session(self):

        # #
        print("running tests for downloading basics")

        # upload the playlists #
        self.manager.UploadPlaylistsFromJSONFiles()

        # we are using a completely copyright free playlist from an open music site #
        # Manipulating this data should be completely licit in any context #
        self.app.run(debug=True)
        # self.downloadDefaultPlaylist()

        print("... finishing session with terminate flag.")
        return  # def createPlaylistEntry():

    # check to make sure that we haven't terminated #
    def RunMaintenanceFunctions(self):

        while not self.terminate:
            self.check_update_status()  # every few minutes we will check to see
            self.writeLog()  # write the log to make sure that everything is going well
            time.sleep(5)

    def runAppOnSocket(self):
        pass

    #  #
    def check_update_status(self):
        print("....checking status....")
        pass
        return

    #  #
    def writeLog(self):

        with open("log.txt", "a") as myfile:
            now = datetime.now()
            time_now = now.strftime("%H:%M:%S")
            myfile.write("log application running..." + str(time_now) + "\n")

    #  #
    def buildDefaultListsFromJSON(self):
        pass
        return
