# from __future__ import unicode_literals
import youtube_dl as yt
import vlc
import time
import os


# copied this code from t
class VLC:
    def __init__(self):
        self.Player = vlc.Instance("--loop")

    def addPlaylistFromDir(self, path):
        self.mediaList = self.Player.media_list_new()
        file_names = os.listdir(path)
        songs = []
        for s in file_names:
            if s.split(".", 1)[1] == "mp3":
                songs.append(s)
            self.mediaList.add_media(self.Player.media_new(os.path.join(path, s)))
        self.listPlayer = self.Player.media_list_player_new()
        self.listPlayer.set_media_list(self.mediaList)

    def play(self):
        self.listPlayer.play()

    def next(self):
        self.listPlayer.next()

    def pause(self):
        self.listPlayer.pause()

    def previous(self):
        self.listPlayer.previous()

    def stop(self):
        self.listPlayer.stop()


# we will document the playlist entries based on tags later #
class PlaylistEntry:
    name = ""
    drive_location = ""


# #
class MediaPlaylistManager:

    # #
    candidateList = []

    def __init__(self):
        self.player = VLC()

    def pullCandidateListsAndTags(self):
        return

    def downloadPlayList(self, playlist_url, directory="default"):
        print("downloading playlist")

        if directory == "default":
            print(
                "no directory specified, using default: "
                + self.default_download_directory
            )

        self.downloader.download([playlist_url])
        return

    def AddAllMp3FromDirectory(self, input_directory):

        return

    def PlayAllFromDirectory(self, input_directory):

        return


# main test function for early functionality
def main():
    playlist = MediaPlaylistManager()
    # dl_cmd.downloadPlayList(playlist_url=playlist_url_input)

    play_directory = "/home/dave/radio_directory/test/"
    playlist.PlayAllFromDirectory(play_directory)


if __name__ == "__main__":
    main()
