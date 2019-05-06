"""
# Author: Howard Webb
# Data: 7/25/2017
# Thermostat controller that reads the temperature sensor and adjusts the exhaust fan

"""
from Humidifier import Humidifier
from scd30 import SCD30
from LogUtil import Logger
import time

class Humidistat(object):
    """Code associated with the thermostat controller"""

    def __init__(self):
        self._logger = Logger("Humidistat")
        self._logger.setLevel(Logger.INFO)
        self._logger.debug("initialize Humidistat object")
        self._co2 = SCD30()
        self._humidifier = Humidifier()

    def check(self, rh=None, test=False):
        """Adjust the fhumidifier depending upon the rh
               Args:
                   temp: optional test rh
               Returns:
                   None
               Raises:
                   None
        """
        target_rh = 80
        if rh == None:
            co2, temp, rh = self._co2.get_data()
            msg = "{} {} {} {}".format("Humidity:", rh, " Target Humidity:", target_rh)
            self._logger.info(msg)    
        if rh > target_rh:
            self._humidifier.set(Humidifier.OFF)
        else:
            self._humidifier.set(Humidifier.ON)

def test(level=Logger.DEBUG):
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """
    test = True
    print("Test")
    ts = Humidistat()
    ts._logger.setLevel(level)
    ts.check(80)
    print("Check Humidity 80")
    time.sleep(10)
    ts.check(99)
    print("Check Humidity 99")
    time.sleep(10)    
    ts.check(None)
    print("Check Humidity None")
    print("Turn Off")
    ts._humidifier.set(OFF)
             
def validate():
    test(Logger.INFO)
    
def main():
    ts = Humidistat()
    ts.check()

if __name__ == "__main__":
    test()



