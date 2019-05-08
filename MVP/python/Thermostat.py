"""
# Author: Howard Webb
# Data: 7/25/2017
# Thermostat controller that reads the temperature sensor and adjusts the exhaust fan

"""
from Fan import Fan
from SI7021 import SI7021
from env import env
from LogUtil import Logger

class Thermostat(object):
    """Code associated with the thermostat controller"""

    def __init__(self):
        self._logger = Logger("Thermostat", lvl=Logger.INFO, file="/home/pi/MVP/logs/state.log")
        self._logger.debug("initialize Thermostat object")
        self._temp = SI7021(self._logger)
        self._fan = Fan(self._logger)

    def check(self, temp=None):
        """Adjust the fan depending upon the temperature
               Args:
                   temp: optional test temperature
               Returns:
                   None
               Raises:
                   None
        """
        if temp == None:
            temp = self._temp.get_tempC()
        # Get target temperature from file
        target_temp = env['thermostat']['targetTemp']
        msg = "{} {} {} {}".format("Temp:", temp, " Target Temp:", target_temp)
        self._logger.info(msg)    
        if temp > target_temp:
            self._fan.set(Fan.ON)
        else:
            self._fan.set(Fan.OFF)

def test(level=Logger.DEBUG):
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """
    print("Test Thermostat")
    ts = Thermostat()
    ts._logger.setLevel(level)
    ts.check(40)
    print("Check Thermostat 40")
    ts.check(20)
    print("Check Thermostat 20")
    ts.check(None)
    print("Check Thermostat None")
    
def validate():
    test(Logger.INFO)

def main():
    ts = Thermostat()
    ts.check()

if __name__ == "__main__":
    main()



