#!/bin/bash

#Script to start up CouchDB
#Author: Howard Webb
#Date: 7/15/2017

# only this line should call this log due to ownership by sudo
# use & at end of file so runs in background
nohup sudo -i -u couchdb /home/couchdb/bin/couchdb 2>&1 | tee -a /home/pi/MVP/logs/couchdb.log &

