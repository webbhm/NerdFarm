#!/bin/bash

#Script to start up the web server
#Author: Howard Webb
#Date: 7/15/2017

#NOTE: The server must be started from the directory from which files are to be served

cd /home/pi/MVP/web

# Note this simple server is the Python3 upgrade.  It works nicely, but doesn't log data
# If you are interested in more logging, you can dig in here:
# https://medium.com/@andrewklatzke/creating-a-python3-webserver-from-the-ground-up-4ff8933ecb96

python3 -m http.server &> /home/pi/MVP/logs/server.log &
