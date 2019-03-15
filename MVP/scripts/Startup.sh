#!/bin/bash

#Script to start up the web server
#This should be placed in a startup directory so it runs every time the Pi is booted
#There are several ways to do this, but the following is one
#https://www.raspberrypi.org/documentation/linux/usage/rc-local.md
#Author: Howard Webb
#Date: 7/15/2017

echo Running Startup

sudo chmod 666 /home/pi/MVP/logs/*

echo Starting CouchDB
# Start CouchDB
/home/pi/MVP/scripts/StartCouchDB.sh >> /home/pi/MVP/logs/startup.log 2>&1

echo Starting Server
# Start Server
/home/pi/MVP/scripts/StartServer.sh >> /home/pi/MVP/logs/startup.log 2>&1

sudo chmod 666 /home/pi/MVP/logs/*

# add sleep to see if this will give time for the couchdb library stuff to get set up.
sleep 10
echo Check Lights, etc
# Run startup code
python3 /home/pi/MVP/python/StartUp.py >> /home/pi/MVP/logs/startup.log 2>&1

