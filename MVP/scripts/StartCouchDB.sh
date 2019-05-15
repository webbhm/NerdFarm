#!/bin/bash

#Script to start up CouchDB
#Author: Howard Webb
#Date: 7/15/2017

sudo -i -u couchdb /home/couchdb/bin/couchdb 2>&1 | tee -a /home/pi/MVP/logs/couchdb.log &

# need to change due to sudo call
sudo chmod 666 /home/pi/MVP/logs/*


