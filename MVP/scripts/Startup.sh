#!/bin/bash

#Script to start up the web server
#This should be placed in a startup directory so it runs every time the Pi is booted
#There are several ways to do this, but the following is one
#https://www.raspberrypi.org/documentation/linux/usage/rc-local.md
#Author: Howard Webb
#Date: 7/15/2017

echo \nRunning Startup >> /home/pi/MVP/logs/startup.log 2>&1

sudo chmod 666 /home/pi/MVP/logs/*

echo Starting CouchDB >> /home/pi/MVP/logs/startup.log 2>&1
# Start CouchDB
/home/pi/MVP/scripts/StartCouchDB.sh >> /home/pi/MVP/logs/startup.log 2>&1

echo Starting Server >> /home/pi/MVP/logs/startup.log 2>&1
# Start Server
/home/pi/MVP/scripts/StartServer.sh >> /home/pi/MVP/logs/startup.log 2>&1

echo Check Lights, etc >> /home/pi/MVP/logs/startup.log 2>&1
# Run startup code
python3 /home/pi/MVP/python/StartUp.py >> /home/pi/MVP/logs/startup.log 2>&1

