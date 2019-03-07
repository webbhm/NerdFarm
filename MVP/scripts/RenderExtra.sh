# Render additions custom for test environment

web_dir="/home/pi/MVP/web/"
python_dir="/home/pi/MVP/python/"
pic2_dir="/home/pi/MVP/pictures_R/"

# Second camera
#Pipe ls of the webcam directory from most recent to latest
# Then clip off only the last line
# Finally trim the string to just the name and store in the variable (File Name)
FN=$(ls -ltr "$pic2_dir" | tail -1 | awk '{print $NF}')

#Check that got what expected
echo "$pic2_dir$FN"

#Finally copy this file to the output web directory
#Since will be overwriting, need to confirm with "yes"
yes | cp "$pic2_dir$FN" "$web_dir"image_R.jpg

# Charting

echo "Build LUX graph"
#create the LUX graph
python3 "$python_dir"LuxChart.py

echo "Build EC graph"
#create the EC graph
python3 "$python_dir"ECChart.py

echo "Build CO2 graph"
#create the CO2 graph
python3 "$python_dir"CO2Chart.py

echo "build Pressure Deficite Graph"
python3 "$python_dir"VPDChart.py


echo "build Growth graph"
#python3 "$python_dir"getSQLMultiAreaChart.py

echo "build Avg Temp graph"
#python3 "$python_dir"getAdjTempChart.py
