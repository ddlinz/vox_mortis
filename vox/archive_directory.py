from __future__ import unicode_literals
from re import I
import youtube_dl as yt
import sys
import os

# a simpler logger for use in stopping exceptions from halting the operation of the download #
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


class ArchiveDirectory:
    #
    # initialization function
    #
    def __init__(self, archive_name="None", archive_master_dir="None"):

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

        # logging the errors so that they don't disuprt the flow of the download #
        loggr = MyLogger()

        # options for the YT downloader #
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
        self.downloader = yt.YoutubeDL(self.ydl_opts)

    #####
    # download Playlists
    #####
    def downloadPlayList(self, playlist_url):

        # #
        print("downloading playlist...")

        # create the directory if it doesn't exisrt #
        if not os.path.exists(self.full_save_directory):
            os.makedirs(self.full_save_directory)
        self.downloader.download([playlist_url])

        # record the information as part of the record #
        info_dict = self.downloader.extract_info(playlist_url, download=False)
        return


#
# main test function for early functionality
#
def main():

    print("running tests for downloading basics")
    dl_cmd = ArchiveDirectory()
    dl_cmd.default_download_directory = "/home/dave/radio_directory"
    print(dl_cmd.default_download_directory)

    playlist_url_input = (
        "https://www.youtube.com/playlist?list=PLRbcQXWEJAJqngAmM0LdWJoehr9X6hdQH"
    )
    dl_cmd.downloadPlayList(playlist_url=playlist_url_input)

    print("done with function")
    return


if __name__ == "__main__":
    main()
