"""
# Author: Howard Webb
# Data: 7/25/2017
# Thermostat controller that reads the temperature sensor and adjusts the exhaust fan

"""
from Fan import Fan, ON, OFF
from scd30 import SCD30
from LogUtil import get_logger

class CO2_stat(object):
    """Code associated with the thermostat controller"""

    def __init__(self):
        self.logger = get_logger("CO2_stat")
        self.logger.debug("initialize CO2 controller object")
        self._co2 = SCD30()
        self._fan = Fan()

    def check(self, co2=None, test=False):
        """Adjust the fan depending upon the CO2
               Args:
                   temp: optional test CO2
               Returns:
                   None
               Raises:
                   None
        """
        target_co2 = 1000
        if co2 == None:
            co2, temp, rh = self._co2.get_data()
        msg = "{} {} {} {}".format("CO2:", co2, " Target CO2:", target_co2)
        # Get target temperature from file
        
        self.logger.info(msg)    
        if co2 > target_co2:
            self._fan.set(ON, test)
        else:
            self._fan.set(OFF, test)

def test():
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """
    print("Test")
    ts = CO2_stat()
    ts.check(800, True)
    print("Check CO2 800")
    ts.check(2000, True)
    print("Check CO2 2000")
    ts.check(None, True)
    print("Check CO2 None")
    
def main():
    ts = CO2_stat()
    ts.check()

if __name__ == "__main__":
    main()


