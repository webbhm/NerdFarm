#!/bin/bash

# Log sensor data to the database

echo
echo $(date +"%D %T") "Log Mushroom Sensors"

#Log std JSON data
python3 /home/pi/MVP/python/LogShroom.py

