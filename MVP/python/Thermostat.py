"""
# Author: Howard Webb
# Data: 7/25/2017
# Thermostat controller that reads the temperature sensor and adjusts the exhaust fan

"""
from Fan import Fan, ON, OFF
from SI7021 import SI7021
from env import env
from LogUtil import get_logger

class Thermostat(object):
    """Code associated with the thermostat controller"""

    def __init__(self):
        self.logger = get_logger("Thermostat")
        self.logger.debug("initialize Thermostat object")
        self._temp = SI7021()
        self._fan = Fan()

    def check(self, temp=None, test=False):
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
        self.logger.info(msg)    
        if temp > target_temp:
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
    ts = Thermostat()
    ts.check(40, True)
    print("Check Thermostat 40")
    ts.check(20, True)
    print("Check Thermostat 20")
    ts.check(None, True)
    print("Check Thermostat None")
    
def main():
    ts = Thermostat()
    ts.check()

if __name__ == "__main__":
    main()



