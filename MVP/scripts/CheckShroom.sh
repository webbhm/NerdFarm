#!/bin/bash

timestamp="$(date +"%D %T")"
echo $(date +"%D %T") "Check Mushroom Environment"

#Log std JSON data
python3 /home/pi/MVP/python/Humidistat.py
python3 /home/pi/MVP/python/CO2_stat.py

