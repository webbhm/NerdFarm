# Code modified from: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/ds18b20
# This code requires modifying /boot/config.txt for modprobe
# add:
# dtoverlay=w1-gpio-pullup
# This code requires using modprobe (see above website)
# This is set up for multiple probes being read (the x in the functions)

import os
import glob
import time
from LogUtil import Logger

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

#for documentation, this is the sensor placement
boxTemp = 3
topTemp = 1
reservoirTemp = 2
ambientTemp = 0

class OneWireTemp(object):

    one_temp = {0:"Ambient", 1: "Reservoir", 2: "Box", 3: "Top"}

    def __init__(self, logger=None):
        """Create sensor object
           Args:
               None
           Returns:
               None
           Raises:
               None
        """        
        self._logger = logger
        if logger == None:
           self._logger = Logger("OneWireTemp", Logger.INFO)
        self._logger.debug("Initialize OneWireTemp")
        # flag for testing
        self._test = False


    def read_temp_raw(self, x):
        """Read sensor buffer
           Args:
               x: number of the sensor
           Returns:
               lines: lines read
           Raises:
               None
        """
        device_folder = glob.glob(base_dir + '28*')[x]
        device_file = device_folder + '/w1_slave'
        self._logger.debug("{} {}, {} {}, {} {}".format("In read temp raw-Device:", x, "Device Folder:", device_folder, "Device File:", device_file)        )
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def getTempC(self, x):
        """Read sensor buffer
           Args:
               x: number of the sensor
           Returns:
               temp_c: temperature reading
           Raises:
               None
        """        
        lines = self.read_temp_raw(x)
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
    #        temp_f = temp_c * 9.0 / 5.0 + 32.0
    #        return temp_c, temp_f
            return temp_c
    
def test():
    print("Test OneWireTemp")
    ow=OneWireTemp()
    ow._logger.setLevel(Logger.DEBUG)
    ow._test=False
    for x in range (0, 4):
        print("Device: " + str(x))
        for y in range(1, 20):
            tempC = ow.getTempC(x)
            print ("Temp : %.2f C" %tempC)
            
def validate():
    print("Validate OneWireTemp")    
    ow=OneWireTemp()
    ow._logger.setLevel(Logger.INFO)
    for x in range (0, 4):
        tempC = ow.getTempC(x)
        ow._logger.info("{}: {} {}: {:3.2f}".format("Device", x, "Temp C", tempC))
    

if __name__=="__main__":
    validate()



