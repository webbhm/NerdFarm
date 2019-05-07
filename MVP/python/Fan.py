"""
# Acuator for the exhaust fan
# Author: Howard Webb
# Date: 2/15/2017
"""

from env import env
from Relay import Relay, FAN_PIN
import time
from LogUtil import Logger
from CouchUtil import CouchUtil

class Fan(object):
    """Code associated with the exhaust fan"""
    ON = 1
    OFF = 0

    target_temp = 0

    def __init__(self, logger=None):
        self._logger = logger
        if logger == None:
           self._logger = Logger("Relay", Logger.INFO)
        self._logger.debug("initialize Fan object")        
        self._relay = Relay(self._logger)
        self.fan_relay = FAN_PIN
        self._couch = CouchUtil(self._logger)
        # flag for testing
        self._test = False
        
    def set(self, state):
        """Set the fan to state
            Args:
                state: condition from other source
            Returns:
                None
            Raises:
                None
        """
        self._logger.debug("In set_state")
        prior = self._relay.get_state(self.fan_relay)
        self._relay.set_state(self.fan_relay, state)
        current = self._relay.get_state(self.fan_relay)
        if prior != current:
            self.log_state(state)

    def set_fan_on(self):
        """Turn the fan on
            Args:
                None
            Returns:
                None
            Raises:
                None
        """
        self._logger.debug("In set_fan_on")
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
        self._logger.debug("In set_fan_off")
        self.set(OFF, test)

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
        self._logger.debug("{}, {:1}, {} {}".format("Fan State Change: Value: ", value, " Status Qualifier: ", status_qualifier))        
        
    def getState(self):
        return self._relay.get_state(self.fan_relay)

def test(level = Logger.DEBUG):
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """
    fan = Fan()
    fan._logger.setLevel(level)
    fan._test = True
    print("Test")
    print("State: " + str(fan.getState()))
    print("Turn Fan On")
    fan.set(fan.ON)
    print("State: " + str(fan.getState()))
    time.sleep(2)

    print("Turn Fan Off")
    fan.set(fan.OFF)
    print("State: " + str(fan.getState()))
    time.sleep(2)

    print("Done")
    
def validate():
    test(Logger.INFO)

if __name__ == "__main__":
    test()


