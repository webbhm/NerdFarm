#!/bin/sh

# Validation Script - exercise standard code
# Author: Howard Webb
# Date: 11/16/2017

#######################################

TARGET=/home/pi/MVP
PYTHON=$TARGET/python

# Declarations
RED='\033[31;47m'
NC='\033[0m'

# Exit on error
error_exit()
{
	echo ${RED} $(date +"%D %T") "${PROGNAME}: ${1:="Unknown Error"}" ${NC} 1>&2
	exit 1
}


########### Validate ######################

echo "##### Running Validation #####"

python3 $PYTHON/Validate.py || error_exit "Failure Validating Python Code"

echo
echo Check Logging
$TARGET/scripts/LogMVP.sh  || error_exit "Failure Logging Data"
#$TARGET/scripts/LogSensorsExtra.sh  || error_exit "Failure Logging Data"

echo
echo Build Charts
$TARGET/scripts/RenderMVP.sh  || error_exit "Failure Building Charts"

echo
echo Run StartUp Script to initialize system
python3 $PYTHON/StartUp.py || error_exit "Failure setting lights"
echo $(date +"%D %T") "StartUp PASSED"
echo DONE

