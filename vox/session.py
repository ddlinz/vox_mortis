from __future__ import unicode_literals
from abc import ABC
from re import I
import time
from vox.archive import archiveManager
from datetime import datetime

# from youtubedl.youtube_dl import YoutubeDL #
from vox.downloader import YTDLDownloader
from flask import Flask, render_template, url_for
from flask_socketio import SocketIO
from multiprocessing import Queue, Process, JoinableQueue

# from vox.flask_app import socketio, create_flask_app
class GeneralVoxSession(ABC):
    def __init__(self):
        pass


class BasicVoxSession(GeneralVoxSession):

    # create the basic objects, most will be set to none at this point #
    def __init__(self):

        # we are going to increment the number of librarian calls in this thread #
        self.number_librarian_calls = 0
        self.manager = archiveManager(None)

    # create the data base manager, this must be done after the flask application is instantiated #
    def initialize_database_archive(self, app):
        self.manager = archiveManager(app)
        return

    # # run the session #
    # def run_session(self):
    #     print("running tests for downloading basics")
    #     # upload the playlists #
    #     # we are using a completely copyright free playlist from an open music site #
    #     # Manipulating this data should be completely licit in any context #
    #     # self.app.run(debug=True)
    #     print("... finishing session with terminate flag.")
    #     return  # def createPlaylistEntry():

    # #
    def run_librarian_process(self):

        #  #
        self.manager.UploadPlaylistsFromJSONFiles()

        # while we haven't terminated, keep the librarian process running in the background #
        self.number_librarian_calls = self.number_librarian_calls + 1
        print("doing librarian stuff..." + str(self.number_librarian_calls))

        return self.number_librarian_calls

    # # check to make sure that we haven't terminated #
    # def RunMaintenanceFunctions(self):

    #     while not self.terminate:
    #         self.check_update_status()  # every few minutes we will check to see
    #         self.writeLog()  # write the log to make sure that everything is going well
    #         time.sleep(5)

    # #
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
