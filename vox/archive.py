from vox.data_entry import PlayListEntry, UserEntry, TrackEntry, TagEntry
from abc import ABC
from vox.downloader import YTDLDownloader
import json

# #
class Manager(ABC):
    #  #
    def __init__(self):
        pass


# this is the class that manages the archive objects #
class archiveManager(Manager):

    # archive manager creates and managers the DB  #
    def __init__(self, app):

        from vox.data_entry import db

        self.db = db

        if not app == None:
            self.db.init_app(app)
            with app.app_context():
                self.db.create_all()

            # create the downloader #
            self.yt_downloader = YTDLDownloader()
            self.yt_downloader.default_download_directory = "/home/dave/radio_directory"

            # set the playlists directory that we will use to upload the initial playlists#
            self.default_playlist_dir = "vox/json/lists.json"

        return

    # create a track entry #
    def createTrackFromURI(self, uri_input, download_track=False):
        print("...creating track entry from URI")

        return

    # #
    def createPlaylistFromURI(self, uri_input, load_tracks, download_tracks=False):
        print("...creating playlist entry from URI")

        new_playlist = PlayListEntry(origin_uri=uri_input)

        # #
        self.db.session.add(new_playlist)
        self.db.session.commit()

        if load_tracks:
            print("downloading tracks...")
            self.createTrackFromURI(uri_input, download_tracks)

        return

    def UploadPlaylistsFromJSONFiles(self):

        with open(self.default_playlist_dir) as json_file:
            dictionary_of_lists = json.load(json_file)

        return
