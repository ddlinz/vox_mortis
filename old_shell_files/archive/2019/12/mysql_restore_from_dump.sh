#!/bin/bash
# declare STRING variable
STRING = $'backing up databases'

#print variable on a screen
echo $STRING

#### REMOTE COMMANDS ####

# get the preference file from the bluehost server 
wget canissociety.org/dump/LocalSettingsBack.php

# get the wikipedia dump from the bluehost server
wget canissociety.org/dump/canissoc_backup_BB
wget canissociety.org/dump/canissoc_backup_wiki

mv canissoc_backup_BB ../core_dumps/canissoc_backup_BB.sql
mv canissoc_backup_wiki ../core_dumps/canissoc_backup_wiki.sql
mv LocalSettingsBack.php ../core_dumps/LocalSettings.php

#### LOCAL COMMANDS ####

# DROP the existing database
sudo mysqladmin -wikiuser -p drop canissoc_wikibase

# create a new database for the user CANISSOC_ROOT
sudo mysqladmin -u wikiuser -p create canissoc_wikibase
sudo mysqladmin -u wikiuser -p create canissoc_phpBB

# drop the old database and create a new one 
sudo mysql -u wikiuser -p canissoc_wikibase < ../core_dumps/canissoc_backup_wiki.sql

# call the update script to purge the wiki
sudo php /var/www/html/wiki/maintenance/update.php

# copy the settings .php from the location in question
sudo cp ../core_dumps/LocalSettings.php /var/www/html/wiki/maintenance/LocalSettings.php
