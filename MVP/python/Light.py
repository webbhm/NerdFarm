#Light Control
# Author: Howard Webb
# Date: 7/25/2017
#Controls the turning on and turning off of lights
#Lights are wired into Relay #4 (Pin 29)

from Relay import *
from LogUtil import Logger
from CouchUtil import CouchUtil

class Light(object):

    def __init__(self, logger=None):
      """Initialize light object
           Args:
               logger: logger object from calling module (if there is one)
           Returns:
               None:
           Raises:
               None
      """
        
      self._logger = logger
      if logger == None:
          self._logger = Logger("Light", Logger.INFO)
      self._relay = Relay(self._logger)
      self._couch = CouchUtil(self._logger)
      
    def set_on(self, test=False):
        """Turn light on (if not already on)
           Args:
               test: indicates test, not to valid create data record
           Returns:
               None:
           Raises:
               None
        """

        if self.get_state()==0:
            self._relay.set_on(lightPin)
            self.log_state("On", test)
            self._logger.debug('Light turned ON')            
        else:
            self._logger.debug('Light already ON - no change')
            
        
    def set_off(self, test=False):
        """Turn light off (if not already off)
           Args:
               test: indicates test, not to valid create data record
           Returns:
               None:
           Raises:
               None
        """
        if self.get_state()==1:
            self._relay.set_off(lightPin)
            self.log_state("Off")
            self._logger.debug('Light turned OFf')                        
        else:
            self._logger.debug('Light already OFF - no change')

    def get_state(self):
        """Check the GPIO
           Args:
               None:
           Returns:
               None:
           Raises:
               None
        """
        return self._relay.get_state(lightPin)

    def log_state(self, value, test=False):
        """Create databse log record
           Args:
               value: (changed) state of the light
           Returns:
               None:
           Raises:
               None
        """
        status_qualifier='Success'
        if test:
            status_qualifier='Test'
        self._couch.saveList(['State_Change','','Top', 'Lights', 'State', value, 'Lights', 'state', status_qualifier, ''])
        self._logger.debug("Log State Change")

def test(level=Logger.DEBUG, test=True):
    """
    System test of the light object
    """
    light=Light()
    light._logger.setLevel(level)
    
    print("Test Light")
    print("Light State: " + str(light.get_state()))
    print("Turn Light On")
    light.set_on(test)
    print("Light State: " + str(light.get_state()))
    print("Turn Light Off")
    light.set_off(test)
    print("Light State: " + str(light.get_state()))
    print("Turn Light On")
    light.set_on(test)
    print("Light State: " + str(light.get_state()))
    print("Done")
    
def validate():
    test(Logger.INFO, False)
    

if __name__=="__main__":
    test()    
                
    

