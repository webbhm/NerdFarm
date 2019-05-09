#!/bin/bash

timestamp="$(date +"%D %T")"

#Script to start up the web server
#This should be placed in a startup directory so it runs every time the Pi is booted
#There are several ways to do this, but the following is one
#https://www.raspberrypi.org/documentation/linux/usage/rc-local.md
#Author: Howard Webb
#Date: 7/15/2017

echo
echo  $(date +"%D %T") Running Startup >> /home/pi/MVP/logs/startup.log 2>&1

sudo chmod 666 /home/pi/MVP/logs/*

echo $(date +"%D %T") Starting CouchDB >> /home/pi/MVP/logs/startup.log 2>&1
/home/pi/MVP/scripts/StartCouchDB.sh

# Give time for the database to get going
sleep(12)

echo $(date +"%D %T") Starting Server >> /home/pi/MVP/logs/startup.log 2>&1
/home/pi/MVP/scripts/StartServer.sh

echo $(date +"%D %T") Check Lights, etc >> /home/pi/MVP/logs/startup.log 2>&1
python3 /home/pi/MVP/python/StartUp.py >> /home/pi/MVP/logs/startup.log 2>&1

