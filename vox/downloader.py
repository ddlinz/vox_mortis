from __future__ import unicode_literals
from abc import ABC
from re import I
import sys
import os
from youtubedl.youtube_dl import YoutubeDL

#from yt-dlp.yt-dlp import YoutubeDLAlt
import vox.data_entry

# # a simpler logger for use in stopping exceptions from halting
# the operation of the download #
class MyLogger(object):
    def __init__(self):
        self._message_queue = []

    def debug(self, msg):
        print("[DEBUG]" + msg)

    def warning(self, msg):
        pass

    def error(self, msg):
        self._message_queue.append(msg)
        print(msg)

    def get_message(self):
        return None if not len(self._message_queue) else self._message_queue.pop()

#
class Downloader(ABC):
    default_download_directory = ""

    # #
    def __init__(self, archive_name="None", archive_master_dir="None"):

        # create a flag that determines whether we want to download to HD, this is default "no"
        self.download_to_hd_enabled = False

        # #
        if archive_name == "None":
            self.archive_name = "test"
        else:
            self.archive_name = archive_name

        # #
        if archive_name == "None" and archive_master_dir == "None":
            self.full_save_directory = "/home/dave/radio_directory/test/"
            print("no directory specified, using default: " + self.full_save_directory)
        elif archive_master_dir == "None":
            self.full_save_directory = "/home/dave/radio_directory/"
            print("no directory specified, using default: " + self.full_save_directory)
        else:
            self.full_save_directory = archive_name + archive_master_dir

        # #
        self.archive_file = (
            self.full_save_directory + self.archive_name + "_archive_file.txt"
        )

    # #
    def set_from_db(self):
        pass

    # #
    def getPlaylistInfo(self, playlist_url):
        pass

# 
class YTDLDownloader(Downloader):

    # initialization function
    def __init__(self, archive_name="None", archive_master_dir="None"):

        super().__init__()

        # logging the errors so that they don't disrupt the flow of the download #
        loggr = MyLogger()

        # options for the YT downloader (transfer to JSON file eventually) #
        self.ydl_opts = {
            "outtmpl": self.full_save_directory + "%(title)s.%(ext)s",
            "quiet": True,
            "download_archive": self.archive_file,
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "ignoreerrors": True,
            "logger": loggr,
        }

        # #
        self.downloader = YoutubeDL({"outtmpl": "%(id)s.%(ext)s"})

    # download Playlists information from a playlist URL #
    def getPlaylistInfo(self, playlist_url):

        # get the playlist information
        print("getting playlist information")

        # create the directory if it doesn't exisrt #
        if not os.path.exists(self.full_save_directory):
            os.makedirs(self.full_save_directory)

        # if self.download_to_hd_enabled: 
        # self.downloader.download([playlist_url])
        # record the information as part of the record 
        try:
            info_dict = self.downloader.extract_info(playlist_url, download=False)
        except:
            print("DOWNLOADER CANNOT OBTAIN PLAYLIST INFORMATION")
            info_dict = None 

        # upload the information to the database #
        return info_dict


    # download the track information in a URI format and save it to the drive
    def downloadTrackArchiveFromURI(self, uri, archive_name, archive_directory): 
        
        try:
            if self.download_to_hd_enabled:
                self.downloader.download([uri]) # download the track to the directory in question
                return 1
            else:
                return -1
        except:
            print("DOWNLOADER CANNOT OBTAIN PLAYLIST INFORMATION")
            pass
        
        return

# # 
# if __name__ == "__main__":
#     print("the default function for the downloader class")
