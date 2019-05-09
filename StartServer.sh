#!/bin/bash

#Script to start up the web server
#This should be placed in a startup directory so it runs every time the Pi is booted
#There are several ways to do this, but the following is one
#https://www.raspberrypi.org/documentation/linux/usage/rc-local.md
#Author: Howard Webb
#Date: 7/15/2017

echo
echo $(date +"%D %T") Starting Server &> /home/pi/MVP/logs/server.log &

#NOTE: The server must be started from the directory from which files are to be served
cd /home/pi/MVP/web
nohup python3 -m http.server &> /home/pi/MVP/logs/server.log &