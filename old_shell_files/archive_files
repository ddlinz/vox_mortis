#!/bin/bash

####################################################################################
# Checks the entered directory ("." is there are no arguments for the script)      #
# The script then creates a directory called "Archive"                             # 
# with sub directories for "$YEAR"/"$MONTH"/"$DAY"                                 #
# the script then copies all of the files to the sub-directory                     #
#day=$(date +%d )
month=$(date +%m )
year=$(date +%Y )

###################################################################################

if [ -z "$1"  ] ; then 
	directory="."	
else 
	directory="~/"$1	
fi

echo $day

if [ ! -d  ""$directory"/archive" ] ; then 
	echo "the archive does not exist yet"
	mkdir "$directory"/archive
fi

if [ ! -d  ""$directory"/archive/"$year"" ] ; then 
	echo "the year directory does not exist yet"
	mkdir "$directory"/archive/"$year"
fi

if [ ! -d ""$directory"/archive/"$year"/"$month"" ] ; then 
	echo "the month directory does not exist yet"
	mkdir "$directory"/archive/"$year"/"$month"
fi

if [ ! -d ""$directory"/archive/"$year"/"$month"/"$day"" ] ; then 
	echo "the day directory does not exist yet"
	mkdir "$directory"/archive/"$year"/"$month"/"$day"
fi

array=( $(  ls -p . | grep -v / ) ) 

for i in "${array[@]}"
do
	cp ./"$i" ./archive/"$year"/"$month"/"$day"
done

####################################################################################
# Script written by David Donovan                                                  #
# December 2019                                                                    #
####################################################################################
