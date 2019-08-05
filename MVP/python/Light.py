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
from CouchUtil import CouchUtil

lightPin = 1

class Light(object):

    def __init__(self, logger=None):
        self._rf = RF_Sender()
        self._logger = logger
        if self._logger == None:
            self._logger = Logger('Light', Logger.INFO, "/home/pi/MVP/logs/obsv.log")
        self._couch = CouchUtil(self._logger)        

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
        self._couch.saveList(['State_Change','','Top', 'Lights', 'State', value, 'Lights', 'state', status_qualifier, ''])            

def test(level=Logger.DEBUG):
    """Self test
           Args:
               None
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
    print("Done")
    
def validate():
    test(Logger.INFO)
    

if __name__=="__main__":
    test()    
                
    

