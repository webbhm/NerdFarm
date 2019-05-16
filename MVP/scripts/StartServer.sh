#!/bin/bash

#Script to start up the web server
#Author: Howard Webb
#Date: 7/15/2017

#NOTE: The server must be started from the directory from which files are to be served

cd /home/pi/MVP/web

# Note the server can be started from a single line (see below), but the python code is called so the logging works
# python3 -m http.server

echo $(date +"%D %T") Starting Web Server >> /home/pi/MVP/logs/server.log
python3 /home/pi/MVP/python/WebServer.py &> /home/pi/MVP/logs/server.log &
