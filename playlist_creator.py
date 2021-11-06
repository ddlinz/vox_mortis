#from __future__ import unicode_literals
#import youtube_dl as yt
import vlc
import time
import os

from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3  
import mutagen.id3  
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER  
  
import glob  

## copied this code from t
class VLC:
    def __init__(self):
       self.Player = vlc.Instance('--loop')
       ## self.Player = vlc.Instance()
    def addPlaylistFromDir(self, path):
        self.mediaList = self.Player.media_list_new()
        file_names = os.listdir(path)
        songs = []
        for s in file_names:
            if s.split(".",1)[1] == "mp3" : 
                songs.append(s)
                self.mediaList.add_media(self.Player.media_new(os.path.join(path,s)))
        self.listPlayer = self.Player.media_list_player_new()
        self.listPlayer.set_media_list(self.mediaList)
    def play(self):
        self.listPlayer.play()
        # self.mediaList.play()
    def next(self):
        self.listPlayer.next()
    def pause(self):
        self.listPlayer.pause()
    def previous(self):
        self.listPlayer.previous()
    def stop(self):
        self.listPlayer.stop()
    def printPlaylist(self): 
        for media_instance in self.mediaList: 
            media_instance.parse()
            print(media_instance.get_meta(12))
            print(media_instance.get_duration())

# we will document the playlist entries based on tags later ##
class PlaylistEntry: 
    name = "" 
    drive_location = ""

## ##
class MediaPlaylistManager:
    
    ## ##
    candidateList = [] 

    ## ##
    def __init__(self) : 
        self.player = VLC()

    ## ##
    def pullCandidateListsAndTags(self):
        return 

    def downloadPlayList(self, playlist_url, directory="default") : 
        print('downloading playlist')

        if directory == "default": 
            print('no directory specified, using default: ' + self.default_download_directory)

        self.downloader.download([playlist_url])
        return
    
    def AddAllMp3FromDirectory(self, input_directory) : 
        return
    
    def PlayAllFromDirectory(self, input_directory) : 

        print('playing everything from the directory {}'.format(input_directory))
        self.player.addPlaylistFromDir(input_directory)


        self.player.printPlaylist()
        self.player.play()

        time.sleep(20)
        self.player.next()
        self.player.play()
        time.sleep(20)
        print('playing')

        return


## main test function for early functionality 
def main():
    playlist = MediaPlaylistManager() 
    play_directory = '/home/dave/radio_directory/test/'
    play_directory = '/home/dave/Dropbox/BloggingFileFolder/Media/Audio/Music-Jazz'
    playlist.PlayAllFromDirectory(play_directory)

if __name__ == "__main__":
    main()

