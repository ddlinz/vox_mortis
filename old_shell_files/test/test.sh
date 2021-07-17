#!/bin/bash          

for x in ~/Dropbox/MediaFileFolder/MusicAndPlaylists/Playlists/YT_game_mix/*.mp3; do 
   echo "$x" 
done

it=0

for x in ~/Dropbox/MediaFileFolder/MusicAndPlaylists/Playlists/YT_game_mix/*.mp3; do 
   y="${x##*/}" 
   z="${y%.*}"
   echo "${z%-*}" 
   echo "${z##*-}" 
   let it=it+1
   echo "$it"
done
