from __future__ import unicode_literals
import youtube_dl as yt
import vlc as vlc


class PlaylistEntry: 
    
    int instance_id
    name = "" 
    drive_location = "" 

## ##
class MediaPlaylistManager:
    ## ##
    candidateList = [] 


    def pullCandidateListsAndTags(self):
        return 

    def downloadPlayList(self, playlist_url, directory="default") : 
        print('downloading playlist')

        if directory == "default": 
            print('no directory specified, using default: ' + self.default_download_directory)

        self.downloader.download([playlist_url])
        return

## main test function for early functionality 
def main():
    playlist = MediaPlaylistManager() 
    ## dl_cmd.downloadPlayList(playlist_url=playlist_url_input)

if __name__ == "__main__":
    main()

