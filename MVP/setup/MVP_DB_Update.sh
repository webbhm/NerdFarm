#!/bin/sh

# CouchDB setup user and start
# Author: Howard Webb
# Date: 11/16/2017

#######################################

TARGET=/home/pi/MVP
PYTHON=$TARTET/python

# Run the release specific build script

# Declarations
RED='\033[31;47m'
NC='\033[0m'

###### Error handler function #######
error_exit()
{
	echo ${RED} $(date +"%D %T") "${PROGNAME}: ${1:="Unknown Error"}" ${NC} 1>&2
	exit 1
}

###### Build #######

#add couchdb user and home
sudo useradd -d /home/couchdb couchdb
# add pi to group so can write to logs
sudo usermod -a -G couchdb pi

# start database
sudo chmod +x $TARGET/scripts/StartCouchDB.sh
$TARGET/scripts/StartCouchDB.sh

echo "##### Give CouchDB some time to start before proceeding #####"
sleep 45


exit 0
