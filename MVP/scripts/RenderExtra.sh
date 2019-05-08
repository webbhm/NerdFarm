#!/bin/bash

timestamp="$(date +"%D %T")"
echo $(date +"%D %T") "Create Extra Charts"

# Render additions custom for test environment

web_dir="/home/pi/MVP/web/"
python_dir="/home/pi/MVP/python/"
pic2_dir="/home/pi/MVP/pictures_R/"

# Charting

echo "Build LUX graph"
python3 "$python_dir"LuxChart.py

echo "Build EC graph"
python3 "$python_dir"ECChart.py

echo "Build CO2 graph"
python3 "$python_dir"CO2Chart.py

echo "build Growth graph"
#python3 "$python_dir"getSQLMultiAreaChart.py

echo "build Avg Temp graph"
#python3 "$python_dir"getAdjTempChart.py
