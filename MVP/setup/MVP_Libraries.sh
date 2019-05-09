#!/bin/sh

# Libraries and Local
# Author: Howard Webb
# Date: 11/16/2017
# Create directories
# Install libraries, including CouchDB and OpenCV

#######################################

TARGET=/home/pi/MVP
PYTHON=$TARGET/python

# Declarations
RED='\033[31;47m'
NC='\033[0m'

# Exit on error
error_exit()
{
	echo ${RED} $(date +"%D %T") "${PROGNAME}: ${1:="Unknown Error"}" ${NC} 1>&2
	exit 1
}

################# Install Libraries ######################
# Make sure back to home directory
cd /home/pi

# Update for latest versions
sudo apt-get update

echo "##### Install Libraries #####"
# FS Webcam
sudo apt-get install fswebcam -y || error_exit "Failure to install fswebcam (USB Camera support)"
echo  $(date +"%D %T") "fswebcam installed (supports USB camera)"

pip install logging || error_exit "Failure to install logging"
echo  $(date +"%D %T") "logging installed"

# Basic GPIO handling - Relay
sudo apt-get install python-rpi.gpio python3-rpi.gpio || error_exit "Failure to install GPIO"
echo $(date +"%D %T") "GPIO Installed"

# Needed for I2C
sudo pip3 install python-periphery || error_exit "Failure to install python-periphery (needed for si7021 temp sensor)"
echo  $(date +"%D %T") "python-periphery installed (needed for si7021 temp sensor)"

# Used for charting
sudo pip3 install pygal|| error_exit "Failure to install pygal (needed for charting)"
echo  $(date +"%D %T") "pygal installed (used for charting)"
#sudo pip3 install pandas|| error_exit "Failure to install pandas (needed for charting)"
#echo  $(date +"%D %T") "pygal installed (used for charting)"

# Used for database access
sudo pip3 install  couchdb || error_exit "Failure to install CouchDB Python library"
echo  $(date +"%D %T") "CouchDB Python Library intalled"

# https://www.raspberrypi.org/forums/viewtopic.php?t=142700
# numpy dependency

#sudo apt-get install python-numpy -y || error_exit "Failure to install numpy math library"
#echo  $(date +"%D %T") "numpy Library intalled"

#sudo apt-get install python-scipy -y || error_exit "Failure to install scipy science library"
#echo  $(date +"%D %T") "scipy Library intalled"

#sudo apt-get install ipython -y || error_exit "Failure to install ipython library"
#echo  $(date +"%D %T") "ipython Library intalled"

#python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose || error_exit "Failure to install pandas, etc (needed for charting)"
sudo pip3 install pandas|| error_exit "Failure to install pandas (needed for charting)"
echo  $(date +"%D %T") "pandas, numpy, etc installed (used for charting)"

##################################################
# Local stuff

echo "##### Build directories #####"
#mkdir -p $TARGET || error_exit "Failure to build MVP directory"
cd $TARGET
mkdir -p data
mkdir -p pictures
echo $(date -u) "directories created"

echo "##### Start Local file changes #####"
# Make scripts executable
chmod +x $TARGET/scripts/*.sh

exit 0
