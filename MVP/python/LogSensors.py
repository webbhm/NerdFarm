'''
Log Optional sensors to CouchDB
Called from /home/pi/MVP/scripts/LogMVP.sh - needs to be uncommented for this to run
Uncomment desired functions in makeEnvObsv
Author: Howard Webb
Date: 5/3/2019
'''

from LogUtil import Logger
from Persistence import Persistence

class LogSensors(object):

    def __init__(self, lvl=Logger.INFO, file="/home/pi/MVP/logs/obsv.log"):
        """Record optional sensor data
        Args:
            lvl: Logging level
        Returns:
            None
        Raises:
            None
        """        
        self._logger = Logger("LogSensors", lvl)
        self._activity_type = "Environment_Observation"
        self._persist = Persistence(self._logger)
        
    def getSI7021(self, test=False):
        """Record temperature and humidity
        Args:
            test: testing flag
        Returns:
            None
        Raises:
            None
        """
        from SI7021 import SI7021            
        si=SI7021()
        # Log temperature
        self._logger.info("Temp-SI7021")                
        try:
            temp = si.get_tempC()

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            rec = ['Environment_Observation', '', 'Top', 'Air', 'Temperature', "{:10.1f}".format(temp), 'Centigrade', 'SI7021', status_qualifier, '']            
            # copy record
            self._persist.save(rec)
            self._logger.debug("{}, {}, {:10.1f}".format("Temp-SI7021", status_qualifier, temp))
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            rec = ['Environment_Observation', '', 'Top', 'Air', 'Temperature', '', 'Centigrade', 'SI7021', status_qualifier, str(e)]
            self._persist.save(rec)            
            self._logger.error("{}, {}, {}".format("Temp-SI7021", status_qualifier, e))

            
        # Log humidity
        self._logger.info("Humidity-SI7021")                
        try:
            humid = si.get_humidity()

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            rec = ['Environment_Observation', '', 'Top', 'Air', 'Humidity', "{:10.1f}".format(humid), 'Percent', 'SI7021', status_qualifier, '']
            self._persist.save(rec)            
            self._logger.debug("{}, {}, {:10.1f}".format("Humidity-SI7021", status_qualifier, humid))

        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            rec = ['Environment_Observation', '', 'Top', 'Air', 'Humidity', '', 'Percent', 'SI7021', status_qualifier, str(e)]
            # copy record
            self._persist.save(rec)            
            self._logger.error("{}, {}, {}".format("Humidity-SI7021", status_qualifier, e))

            
    def log(self, test=False):
        '''Logsensors
            Uncomment desired sensors
            Imports are in the function to avoid loading unnecessary code
        '''

        self.getSI7021(test)
        
def main():
    '''
        Function that should get called from scripts
    '''

    lg = LogSensors(Logger.INFO)
    lg.log()

def validate():
    '''
        Quick test to check working properly
    '''
    
    lg = LogSensors(Logger.DEBUG)
    lg.log()
    
def test():
    '''
        Use for debugging when need detailed output
    '''
    
    test = True
    lg = LogSensors(Logger.DETAIL)
    lg.log(test)

if __name__=="__main__":
    main()
