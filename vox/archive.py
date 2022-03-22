from vox.data_entry import PlayListEntry, UserEntry, TrackEntry, TagEntry, TrackPlaylistLink, ArchiveEntry, TrackArchiveLink,FillInDictionaryWithRequiredFields
from abc import ABC
from vox.downloader import YTDLDownloader
import json
from pathlib import Path
from datetime import datetime


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
        self.default_save_super_directory =  str(Path.home()) + "/vox_save_directory"

        # #
        if not app == None:
            self.db.init_app(app)
            with app.app_context():
                self.db.create_all()

            # create the downloader
            self.yt_downloader = YTDLDownloader()
            self.yt_downloader.default_download_directory = "/home/dave/radio_directory"

            # set the playlists directory that we will use to upload the initial playlists 
            # self.sample_playlist_dir = 

        return

    # create a track entry #
    def createTrackFromURI(self, uri_input, download_track=False):
        print("...creating track entry from URI")

        data_input = None
        self.createTrackFromFullInput(data_input, download_track=download_track)

        return


    def createArchiveEntryFromInput(self, archive_address, track_id=0, mode="uri", platform="youtube"):
        # print("creating archive object here")

        # #
        new_archive = ArchiveEntry(path=archive_address, archive_type="youtube")

        # add an archive entry #
        with self.app.app_context():  
            if self.db.session.query(ArchiveEntry.path).filter_by(path=archive_address).first() is None :
                self.db.session.add(new_archive)
                self.db.session.commit()   

            updated_archive= self.db.session.query(ArchiveEntry).filter_by(path=archive_address).first()
             
            if self.db.session.query(TrackArchiveLink).filter_by(archive_id=updated_archive.id, track_id=track_id):
                new_track_playlist_link = TrackArchiveLink(archive_id=updated_archive.id, track_id=track_id)
                self.db.session.add(new_track_playlist_link)
                self.db.session.commit()

        return

    def createTrackFromFullInput(self, data_input, playlist_id=0, download_track=False) :

        # data for the entries contain the following information that we might want to track here #
        # dict_keys(['id', 'title', 'formats', 'thumbnails', 'description', 'upload_date', 'uploader', 'uploader_id', 'uploader_url',
        # 'channel_id', 'channel_url', 'duration', 'view_count', 'average_rating', 'age_limit', 'webpage_url', 'categories', 'tags', 'is_live', 'like_count', 'channel', 'extractor', 'webpage_url_basename', 'extractor_key', 'n_entries', 'playlist', 'playlist_id', 'playlist_title', 'playlist_uploader', 'playlist_uploader_id', 'playlist_index', 'thumbnail', 'display_id', 'requested_subtitles', 
        # 'requested_formats', 'format', 'format_id', 'width', 'height', 'resolution', 'fps', 'vcodec', 'vbr', 'stretched_ratio', 
        # 'acodec', 'abr', 'ext'])
        
        # new_track = TrackEntry(relative_path=data_input['webpage_url'], origin_uri=data_input['webpage_url'],playlist_origin=playlist_id)
        new_track = TrackEntry(origin_uri=data_input['webpage_url'],
                                playlist_origin=playlist_id,
                                artist=data_input['artist'],
                                album=data_input['album'],
                                title=data_input['title'])

        with self.app.app_context():  

            # update the track #
            if self.db.session.query(TrackEntry.origin_uri).filter_by(origin_uri=data_input['webpage_url']).first() is None :
                self.db.session.add(new_track)
                self.db.session.commit()
            updated_track = self.db.session.query(TrackEntry).filter_by(origin_uri=data_input['webpage_url']).first()

            # track_id = db.Column(db.Integer, db.ForeignKey('track_entry.id'))
            # playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))commit()commit()commit()
            if self.db.session.query(TrackPlaylistLink).filter_by(track_id=updated_track.id,playlist_id=playlist_id):
                new_track_playlist_link = TrackPlaylistLink(track_id=updated_track.id,playlist_id=playlist_id)
                self.db.session.add(new_track_playlist_link)
                self.db.session.commit()

            self.createArchiveEntryFromInput(archive_address=updated_track.origin_uri, track_id=updated_track.id)
         
        #print("creating track entry from ")
        return updated_track


    def createPlaylistFromData(self, data, write_playlist_data_to_file=True):

        # write the returned data to an output file #
        if write_playlist_data_to_file :
            with open("vox/playlists/dumped_playlist.json", "w") as outfile:
                json.dump(data, outfile)

        from vox.data_entry import track_template
        #  #
        new_playlist = PlayListEntry(origin_uri=data['webpage_url'])

        #  #
        with self.app.app_context():   
            if self.db.session.query(PlayListEntry.origin_uri).filter_by(origin_uri=data['webpage_url']).first() is None :
                self.db.session.add(new_playlist)
                self.db.session.commit()
            updated_playlist = self.db.session.query(PlayListEntry).filter_by(origin_uri=data['webpage_url']).first()

        #  #
        if not data==None:
            for entry in data['entries'] : 
                entry = FillInDictionaryWithRequiredFields(entry, track_template)
                self.createTrackFromFullInput(entry, updated_playlist.id)

        return

    # #
    def createPlaylistFromURI(self, uri_input):
        
         # get the data from the downloader # 
        #print("...creating playlist entry from URI")
        data = self.yt_downloader.getPlaylistInfo(uri_input)

        self.createPlaylistFromData(data)

        return


    # #
    def createPlaylistFromDirectory(self, input, load_tracks=False, download_tracks=False):
        print("...creating playlist entry from Directory")

        from vox.data_entry import playtlist_template, track_template
        data = playtlist_template.copy()

        from re import search 
        from os import listdir
        import os
        import eyed3


        data['title'] = search('([^/]+$)', input)[0]
        data['webpage_url'] = input
        data['extractor'] = 'vox_hd_entry'

        for file in listdir(input):
            if os.path.isfile((input + "/" + file)) :
                new_template = track_template.copy()
                new_template['webpage_url'] = (input + "/" + file)
                if file.split(".")[1] == "mp3" :
                    audio_info = eyed3.load(new_template['webpage_url'])
                    new_template['title'] = audio_info.tag.title
                    new_template['artist'] = audio_info.tag.artist
                    new_template['album'] = audio_info.tag.album
                    new_template['track'] = audio_info.tag.album
              

                # 
                data['entries'].append(new_template)
            pass

        self.createPlaylistFromData(data)

        return

    # #
    def createPlaylistFromJSON(self, uri_input, load_tracks=False, download_tracks=False):
        print("...creating playlist entry from JSON")
        return

    # #
    def UploadDefaultPlaylists(self):
        # collect all of the non directory files here 
        files_in_playlist_directory = os.listdir(self.default_playlist_dir)
        for file in files_in_playlist_directory: 
            self.UploadPlaylistsFromJSONFiles(file)
        return

    # needs to be be fixed #
    def UploadPlaylistsFromJSONFiles(self, playlist_desc_file, entry_limit =2):

        entry_count = 0 
        print("")
        with open(playlist_desc_file) as json_file:
            dictionary_of_lists = json.load(json_file)

        for entry in dictionary_of_lists['address']:
            if entry['type'] == 'uri':
                self.createPlaylistFromURI(entry['location'])
            elif entry['type'] == 'json':
                self.createPlaylistFromJSON(entry['location'])
            elif entry['type'] == 'directory':
                self.createPlaylistFromDirectory(entry['location'])
            else:
                print("ERROR PASS")

            entry_count = entry_count + 1
            if entry_count >=  entry_limit:
                break

        return


    # create local file for each of the tracks that are marked for download #
    def createArchieEntriesFromTracks(self):
        
        with self.app.app_context():  
            tracks = self.db.session.query(TrackEntry)
            print("")

        return
        # track = TrackEntry.query.get_or_404(id)
        # if request.method == "POST":
        #     track.relative_path = request.form["content"]
        #     try:
        #         db.session.commit()
        #         return redirect("/")
        #     except SystemExit:
        #         return "there was an issue updating the track information"
        # else:
        #     return render_template("update.html", track=track)


    # create an archive from a track entry
    def createArcvhiveEntryFromTrackEntry(self, TrackEntry):
        pass 
