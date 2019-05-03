#!/bin/bash
# MVP specific data logging files

timestamp="$(date +"%D %T")"
echo $(date +"%D %T") "Log Sensors"

#Log std JSON data
python3 /home/pi/MVP/python/LogSensors.py

#Log optional sensors
# Uncomment this (and the particular sensors) to log these options
#python3 /home/pi/MVP/python/LogSensorsExtra.py

