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
        self.app =app

        #  #
        if not app == None:
            self.db.init_app(app)
            with app.app_context():
                self.db.create_all()

            # create the downloader #
            self.yt_downloader = YTDLDownloader()
            self.yt_downloader.default_download_directory = "/home/dave/radio_directory"

            # set the playlists directory that we will use to upload the initial playlists#
            self.default_playlist_dir = "vox/json/initial_playlists.json"

        return

    # create a track entry #
    def createTrackFromURI(self, uri_input, download_track=False):
        print("...creating track entry from URI")

        data_input = None
        self.createTrackFromFullInput(data_input, download_track=download_track)

        return

    # maybe don't use this #  
    def createTrackFromFullInput(self, data_input, download_track=False):

        ## data for the entries 
        # dict_keys(['id', 'title', 'formats', 'thumbnails', 'description', 'upload_date', 'uploader', 'uploader_id', 'uploader_url',
        # 'channel_id', 'channel_url', 'duration', 'view_count', 'average_rating', 'age_limit', 'webpage_url', 'categories', 'tags', 'is_live', 'like_count', 'channel', 'extractor', 'webpage_url_basename', 'extractor_key', 'n_entries', 'playlist', 'playlist_id', 'playlist_title', 'playlist_uploader', 'playlist_uploader_id', 'playlist_index', 'thumbnail', 'display_id', 'requested_subtitles', 
        # 'requested_formats', 'format', 'format_id', 'width', 'height', 'resolution', 'fps', 'vcodec', 'vbr', 'stretched_ratio', 
        # 'acodec', 'abr', 'ext'])

        
        new_track = TrackEntry(relative_path=data_input['webpage_url'], origin_uri=data_input['webpage_url'])
        
        with self.app.app_context():  
            if self.db.session.query(TrackEntry.origin_uri).filter_by(origin_uri=data_input['webpage_url']).first() is None :
                self.db.session.add(new_track)
                self.db.session.commit()

        print("creating track entry from ")
        return

    # #
    def createPlaylistFromURI(self, uri_input, load_tracks=False, download_tracks=False):
        
        print("...creating playlist entry from URI")
        new_playlist = PlayListEntry(origin_uri=uri_input)


        print('createing playlist')
        # # #
        with self.app.app_context():       
            if self.db.session.query(PlayListEntry.origin_uri).filter_by(origin_uri=uri_input).first() is None :
                self.db.session.add(new_playlist)
                self.db.session.commit()

        # if load_tracks:
        #     print("downloading tracks...")
        #     self.createTrackFromURI(uri_input, download_tracks)

        data = self.yt_downloader.downloadPlayList(uri_input)

        for entry in data['entries'] : 
            self.createTrackFromFullInput(entry)

        return

    def UploadPlaylistsFromJSONFiles(self):

        entry_limit = 2
        entry_count = 0 
        print("")
        with open(self.default_playlist_dir) as json_file:
            dictionary_of_lists = json.load(json_file)

        for entry in dictionary_of_lists['address']:
            self.createPlaylistFromURI(entry['uri'])
            entry_count = entry_count + 1
            if entry_count >=  entry_limit:
                break

        return
