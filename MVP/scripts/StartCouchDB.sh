#!/bin/bash

#Script to start up CouchDB
#Author: Howard Webb
#Date: 7/15/2017

echo
echo  $(date +"%D %T") Starting CouchDB >> /home/pi/MVP/logs/startup.log 2>&1

nohup sudo -i -u couchdb /home/couchdb/bin/couchdb &> /home/pi/MVP/logs/couchdb.log &

