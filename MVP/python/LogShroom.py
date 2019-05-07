""" Log standard MVP sensors
"""

from CouchUtil import CouchUtil
from LogUtil import Logger

class LogShroom(object):

    def __init__(self, logger=None):
        """Create sensor object
           Args:
               None
           Returns:
               None
           Raises:
               None
        """        
        self._logger = logger
        if logger == None:
           self._logger = Logger("LogShroom", Logger.INFO)
        self._logger.debug("Initialize LogShroom")
        self._couch = CouchUtil(self._logger)
        # flag for testing
        self._test = False
    
    
    def log(self):
        """Routine to log all sensors
        Args:
            None
        Returns:
            None
        Raises:
            None
        """               
        self.getSCD()
        
    def getSCD(self):
        """Record CO2 sensor (scd30)
            Generates co2, temperature and relative humidity
        Args:
            None
        Returns:
            None
        Raises:
            None
        """           
        
        from scd30 import SCD30
        self._scd = SCD30(self._logger)
        self._logger.debug("In SCD30")
        try:
            co2, temp, rh = self._scd.get_data()

            status = 'Success'
            if self._test:
                status = 'Test'
            self._couch.saveList(['Environment_Observation', '', 'Top', 'Air', 'CO2', "{:10.1f}".format(co2), 'ppm', 'scd30', status, ''])
            self._couch.saveList(['Environment_Observation', '', 'Top', 'Air', 'Temperature', "{:10.1f}".format(temp), 'Centigrade', 'scd30', status, ''])
            self._couch.saveList(['Environment_Observation', '', 'Top', 'Air', 'Humidity', "{:10.1f}".format(rh), 'Percent', 'scd30', status, ''])
            self._logger.info("{} {:6.1f}, {} {:3.1f}, {} {:3.1f}".format("EnvObsv-CO2:", co2, "Temp", temp, "Humidity:", rh))            
        except Exception as e:
            status = 'Failure'
            if self._test:
                status = 'Test'
            self._couch.saveList(['Environment_Observation', '', 'Top', 'Air', 'CO2', '', 'ppm', 'scd30', status, str(e)])                            
            self._couch.saveList(['Environment_Observation', '', 'Top', 'Air', 'Temperature', '', 'Centigrde', 'scd30', status, ''])
            self._couch.saveList(['Environment_Observation', '', 'Top', 'Air', 'Humidity', '', 'Percent', 'scd30', status, ''])
            self._logger.debug("{} {}".format("EnvObsv-SCD30 Error:", e))            
                                                                       

def test():
    print("Testing SDC30")
    ls = LogShroom()
    ls._logger.setLevel(Logger.DEBUG)
    ls._test = True
    ls.log()
    
def validate():
    print("Validate SDC30")    
    main(Logger.INFO)
    
def main(level=Logger.INFO):    
    ls = LogShroom()
    ls._logger.setLevel(level)
    ls.log()

if __name__=="__main__":
    main()    
