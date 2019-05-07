"""
# Acuator for the exhaust fan
# Author: Howard Webb
# Date: 2/15/2017
"""

from Relay import *
import time
from LogUtil import Logger
from CouchUtil import CouchUtil

class Humidifier(object):
    """Code associated with the Humidifier"""

    ON = 1
    OFF = 0
    target_rh = 0

    def __init__(self, logger=None):
        self._logger = logger
        if logger == None:
            self._logger = Logger("Humidifier", Logger.INFO)
        self._logger.debug("initialize Fan object")
        self._relay = Relay(self._logger)
        self._pin = 29
        self._couch = CouchUtil(self._logger)
        # flag for if in testing
        self._test = False

    def set(self, state):
        """Set the humidifier to state
            Args:
                state: condition from other source
            Returns:
                None
            Raises:
                None
        """
        self._logger.debug("In set_state")
        self._relay.set_state(self._pin, state)

        

    def set_on(self):
        """Turn the humidifier on
            Args:
                None
            Returns:
                None
            Raises:
                None
        """
        self._logger.debug("In set_on")
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
        self._logger.debug("In set_off")
        self.set(OFF, test)
        
    def get_state(self):
        return self._relay.get_state(self._pin)

    def log_state(self, value):
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
        if self._test:
            status_qualifier = 'Test'
        self._couch.saveList(['State_Change', '', 'Side', 'Fan', 'State', value, 'state', 'Fan', status_qualifier, ''])

def test(level=Logger.DEBUG):
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """
    hm = Humidifier()
    hm._test = True
    hm._logger.setLevel(level)
    print("Test")
    print("State: " + str(hm.get_state()))
    print("Turn Humidifier On")
    hm.set(Humidifier.ON)
    print("State: " + str(hm.get_state()))
    time.sleep(10)

    print("Turn Humidifier Off")
    hm.set(Humidifier.OFF)
    print("State: " + str(hm.get_state()))
    time.sleep(2)

    print("Done")
    
def validate():
    test(Logger.INFO)
    
if __name__ == "__main__":
    validate()


