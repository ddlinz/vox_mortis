#! /bin/bash
# declare STRING 
STRING1=$'Remotely log in and dump the database and preference files to the open https folder'
STRING2=$'All dumped files can be found on https://www.canissociety.org/dump/'

echo $STRING1
echo $STRING2

ssh canissoc@canissociety.org ./dump_script.sh

echo 'operation completed.'
