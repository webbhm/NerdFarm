"""
# Acuator for the exhaust fan
# Author: Howard Webb
# Date: 2/15/2017
"""

from env import env
from Relay import *
import time
from LogUtil import get_logger
from CouchUtil import saveList

ON = 1
OFF = 0

class Fan(object):
    """Code associated with the exhaust fan"""

    relay = None
    target_temp = 0

    def __init__(self):
        self.logger = get_logger("Fan")
        self.logger.debug("initialize Fan object")
        self.relay = Relay()
        self.fan_relay = fanPin

    def set(self, state, test=False):
        """Set the fan to state
            Args:
                state: condition from other source
            Returns:
                None
            Raises:
                None
        """
        self.logger.debug("In set_state")
        self.relay.set_state(self.fan_relay, state)

        

    def set_fan_on(self, test=False):
        """Turn the fan on
            Args:
                None
            Returns:
                None
            Raises:
                None
        """
        self.logger.debug("In set_fan_on")
        self.set(ON, test)

    def set_fan_off(self):
        """Turn the fan off
            Args:
                None
            Returns:
                None
            Raises:
                None
        """
        self.logger.debug("In set_fan_off")
        self.set(OFF, test)

    def log_state(self, value, test=False):
        """Send state change to database
           Args:
               value: state change
               test: flag for testing
           Returns:
               None
           Raises:
               None
        """
        status_qualifier = 'Success'
        if test:
            status_qualifier = 'Test'
        saveList(['State_Change', '', 'Side', 'Fan', 'State', value, 'state', 'Fan', status_qualifier, ''])

def test():
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """
    fan = Fan()
    print("Test")
    print("State: " + str(fan.relay.get_state(fan.fan_relay)))
    print("Turn Fan On")
    fan.set(ON, test)
    print("State: " + str(fan.relay.get_state(fan.fan_relay)))
    time.sleep(2)

    print("Turn Fan Off")
    fan.set(OFF)
    print("State: " + str(fan.relay.get_state(fan.fan_relay)))
    time.sleep(2)

    print("Done")

if __name__ == "__main__":
    test()


