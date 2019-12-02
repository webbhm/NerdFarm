'''
Pump control - modification of Light.py, same RF, different signal
# Author: Howard Webb
# Date: 8/05/2019
Controls the turning on and turning off of pump via RF
Pump use RF Plug #2
There is no way to check the state with the RF
'''

from RF_Send import RF_Sender
from LogUtil import Logger
from Persistence import Persistence

pumpPin = 2

class Pump(object):

    def __init__(self, logger=None):
        self._rf = RF_Sender()
        self._logger = logger
        if self._logger == None:
            self._logger = Logger('Pump', Logger.INFO, "/home/pi/MVP/logs/obsv.log")
        self._persist = Persistence(self._logger)
        
    def __del__(self):
        '''
        Don't call GPIO.cleanup() as need to leave pin state as is
        '''
        pass

    def on(self, test=False):
        "Check state and turn on if needed"
        self._rf.set_on(pumpPin,)
        self.log_state("On", test)
        self._logger.debug('Pump turned ON')            
            
        
    def off(self, test=False):
        '''Check state and turn off if needed'''
        self._rf.set_off(pumpPin)
        self.log_state("Off", test)
        self._logger.debug('Pump turned Off')                        

    def log_state(self, value, test=False):
        """
        Create Environment Observation
    """
        status_qualifier='Success'
        if test:
            status_qualifier='Test'
        self._persist.save(['State_Change','','Reservoir', 'Pump', 'State', value, 'Pump', 'state', status_qualifier, ''])                    


def test(level=Logger.DEBUG):
    """Self test
           Args:
               None
           Returns:
               None
           Raises:
               None
    """

    pmp=Pump()
    pmp._logger.setLevel(level)    
    
    print("Test Pump")
    print("Turn Pump On")
    pmp.on(True)
    print("Turn Pump Off")
    pmp.off(True)
    print("Done")
    
def validate():
    test(Logger.INFO)
    

if __name__=="__main__":
    test()    
                
    

