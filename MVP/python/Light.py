'''
#Light Control
# Author: Howard Webb
# Date: 8/05/2019
Controls the turning on and turning off of lights via RF
Lights use RF Plug #1
There is no way to check the light state with the RF
'''

from RF_Send import RF_Sender
from LogUtil import Logger
from Environ import Environ
from Persistence import Persistence

lightPin = 1 #RF Switch

class Light(object):

    def __init__(self, logger=None):
        self._logger = logger
        if self._logger == None:
            self._logger = Logger('Light', Logger.INFO, "/home/pi/MVP/logs/obsv.log")
            self._logger.debug("Initialize RF Light")
        self._rf = RF_Sender(self._logger)
        self._persist = Persistence(self._logger)
        
    def __del__(self):
        self._rf.cleanup()

    def set_on(self, test=False):
        "Check state and turn on if needed"
        self._rf.set_on(lightPin,)
        self.log_state("On", test)
        self._logger.debug('Light turned ON')            
        
    def set_off(self, test=False):
        '''Check state and turn off if needed'''
        self._rf.set_off(lightPin)
        self.log_state("Off", test)
        self._logger.debug('Light turned Off')                        

    def log_state(self, value, test=False):
        """
        Create Environment Observation
    """
        status_qualifier='Success'
        if test:
            status_qualifier='Test'
        self._persist.save(['State_Change','','Top', 'Lights', 'State', value, 'Boolean', 'Light', status_qualifier, ''])
        
    def check(self):
        env = Environ(self._logger)
        if env._state:
            self.set_on(test)
        else:
            self.set_off(test)

def test(level=Logger.DEBUG):
    """Self test
           Args:
               level - debug display level
           Returns:
               None
           Raises:
               None
    """

    lght=Light()
    lght._logger.setLevel(level)    
    
    print("Test Light")
    print("Turn Light On")
    lght.set_on(True)
    print("Turn Light Off")
    lght.set_off(True)
    print("Turn Light On")
    lght.set_on(True)
    print("Check what should be")
    lght.check()
    print("Done")
    
def validate():
    test(Logger.INFO)
    

if __name__=="__main__":
    test()    
                
    

