#!/bin/sh

# Main Release Scrip
# Author: Howard Webb
# Date: 11/16/2017
# Updated 2/24/2019
# Create directories
# Install libraries, including CouchDB and OpenCV
# Set up variables
# Test the System
# Load cron to automate

#######################################

TARGET=/home/pi/MVP
PYTHON=$TARGET/python

##### Error Handling Function #####

# Declarations
RED='\033[31;47m'
NC='\033[0m'

# Exit on error
error_exit()
{
	echo ${RED} $(date +"%D %T") "${PROGNAME}: ${1:="Unknown Error"}" ${NC} 1>&2
	exit 1
}

############################################333

echo "##### Release Script #####"

echo "###### Update the system ######"
sudo apt-get update

echo "###### Set Permissions ######"
sudo chmod +x $TARGET/setup/*.sh

# Comment out the next two lines for complete automatic build, else will exit here
#echo  "###### Exit without running release ######"
#exit 0

echo  "###### Install CouchDB ######"
$TARGET/setup/CouchDB.sh || error_exit "Failure installing CouchDB"

echo  "###### Install Libraries and Local changes ######"
$TARGET/setup/ReleaseScript_Local.sh || error_exit "Failure installing libraries"

echo  "###### Test ######"
$TARGET/setup/ReleaseScript_Test.sh || error_exit "Failure on testing"

echo  "###### Final Configuration ######"
$TARGET/setup/ReleaseScript_Final.sh || error_exit "Failure on final configuration"

echo "##### Release Install Completed Successfully, You should reboot the system #####"

exit 0

