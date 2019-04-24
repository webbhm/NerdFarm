"""
# Author: Howard Webb
# Data: 7/25/2017
# Thermostat controller that reads the temperature sensor and adjusts the exhaust fan

"""
from Humidifier import Humidifier, ON, OFF
from scd30 import SCD30
from LogUtil import get_logger
import time

class Humidistat(object):
    """Code associated with the thermostat controller"""

    def __init__(self):
        self.logger = get_logger("Humidistat")
        self.logger.debug("initialize Humidistat object")
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
            
        self.logger.info(msg)    
        if rh > target_rh:
            self._humidifier.set(OFF, test)
        else:
            self._humidifier.set(ON, test)

def test():
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
    ts.check(80, True)
    print("Check Humidity 80")
    time.sleep(10)
    ts.check(99, True)
    print("Check Humidity 99")
    time.sleep(10)    
    ts.check(None, True)
    print("Check Humidity None")
    print("Turn Off")
    ts._humidifier.set(OFF, test)
    
def main():
    ts = Humidistat()
    ts.check()

if __name__ == "__main__":
    main()



