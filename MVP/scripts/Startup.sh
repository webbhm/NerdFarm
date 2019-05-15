#!/bin/bash

# Routines for when the Raspberry is first started
# This is called from /etc/rc.local
#https://www.raspberrypi.org/documentation/linux/usage/rc-local.md
#Author: Howard Webb
#Date: 7/15/2017

echo
echo  $(date +"%D %T") Running Startup >> /home/pi/MVP/logs/startup.log

echo $(date +"%D %T") Starting CouchDB >> /home/pi/MVP/logs/startup.log
/home/pi/MVP/scripts/StartCouchDB.sh

# Give time for the database to get going
echo "Sleeping 20" >> /home/pi/MVP/logs/startup.log
sleep 20

echo $(date +"%D %T") Starting Server >> /home/pi/MVP/logs/startup.log
/home/pi/MVP/scripts/StartServer.sh

echo $(date +"%D %T") Check Lights, etc >> /home/pi/MVP/logs/startup.log
python3 /home/pi/MVP/python/StartUp.py  2>&1 | tee -a /home/pi/MVP/logs/startup.log

