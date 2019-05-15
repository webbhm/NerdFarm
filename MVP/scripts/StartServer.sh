#!/bin/bash

#Script to start up the web server
#Author: Howard Webb
#Date: 7/15/2017

#NOTE: The server must be started from the directory from which files are to be served
cd /home/pi/MVP/web

echo
echo  $(date +"%D %T") Starting Server >> /home/pi/MVP/logs/server.log

# run in background so other processes in the calling script get run
python3 -m http.server 2>&1 | tee -a /home/pi/MVP/logs/server.log &
