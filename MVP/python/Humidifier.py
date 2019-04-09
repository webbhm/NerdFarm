"""
# Acuator for the exhaust fan
# Author: Howard Webb
# Date: 2/15/2017
"""

from Relay import *
import time
from LogUtil import get_logger
#from CouchUtil import saveList

ON = 1
OFF = 0

class Humidifier(object):
    """Code associated with the Humidifier"""

    relay = None
    target_rh = 0

    def __init__(self):
        self.logger = get_logger("Humidifier")
        self.logger.debug("initialize Fan object")
        self.relay = Relay()
        self._relay = 29

    def set(self, state, test=False):
        """Set the humidifier to state
            Args:
                state: condition from other source
            Returns:
                None
            Raises:
                None
        """
        self.logger.debug("In set_state")
        self.relay.set_state(self._relay, state)

        

    def set_on(self, test=False):
        """Turn the humidifier on
            Args:
                None
            Returns:
                None
            Raises:
                None
        """
        self.logger.debug("In set_on")
        self.set(ON, test)

    def set_off(self):
        """Turn the fan off
            Args:
                None
            Returns:
                None
            Raises:
                None
        """
        self.logger.debug("In set_off")
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
        #saveList(['State_Change', '', 'Side', 'Fan', 'State', value, 'state', 'Fan', status_qualifier, ''])

def test():
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """
    hm = Humidifier()
    print("Test")
    print("State: " + str(hm.relay.get_state(hm._relay)))
    print("Turn Humidifier On")
    hm.set(ON, test)
    print("State: " + str(hm.relay.get_state(hm._relay)))
    time.sleep(10)

    print("Turn Humidifier Off")
    hm.set(OFF)
    print("State: " + str(hm.relay.get_state(hm._relay)))
    time.sleep(2)

    print("Done")

if __name__ == "__main__":
    test()


