'''
Log Optional sensors to CouchDB
Called from /home/pi/MVP/scripts/LogMVP.sh - needs to be uncommented for this to run
Uncomment desired functions in makeEnvObsv
Author: Howard Webb
Date: 5/3/2019
'''

from CouchUtil import CouchUtil
from LogUtil import Logger

class LogSensorExtra(object):

    def __init__(self, lvl=Logger.INFO):
        """Record optional sensor data
        Args:
            lvl: Logging level
        Returns:
            None
        Raises:
            None
        """        
        self._logger = Logger("LogSensor-Extra", lvl)
        self._activity_type = "Environment_Observation"
        self._dbLogger = CouchUtil(self._logger)
        
    def getOneWire(self, test=False):
        """Loop OneWire temperature sensors
            Assumes there are four
        Args:
            test: flag for testing
        Returns:
            None
        Raises:
            None
        """        
        from oneWireTemp import one_temp
        for sensor in one_temp:
            msg = "Sensor: " + one_temp[sensor]
            self._logger.info(msg)
            self.logOneWire(sensor, one_temp[sensor])
            
    def logOneWire(self, sensor, name, test=False):
        """Record OneWire temperature sensor
        Args:
            sensor: number of the sensor
            name: name of the sensor
            test: flag for testing
        Returns:
            None
        Raises:
            None
        """           
        from oneWireTemp import getTempC
        try:
            temp = getTempC(sensor)

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            self._dbLogger.saveList([self._activity_type, '', name, 'Air', 'Temperature', "{:10.1f}".format(temp), 'Centigrade', 'DS18B20-' + str(sensor), status_qualifier,''])
            self._logger.debug("{}, {}, {:10.1f}".format(name, status_qualifier, temp))                                    
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            self._dbLogger.saveList([self._activity_type, '', name, 'Air', 'Temperature', '', 'Centigrade', 'DS18B20-' + str(sensor), status_qualifier, str(e)])            
            self._logger.error("{}, {}, {}".format(name, status_qualifier, e))                                            

    def getLux(self, test=False):
        """Record LUX sensor (TSL2561)
        Args:
            test: flag for testing
        Returns:
            None
        Raises:
            None
        """           
        from TSL2561 import TSL2561        
        lx = TSL2561()
        self._logger.info("TSL2561 - LUX")
        
        try:
            lux = lx.getLux()
            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            self._dbLogger.saveList([self._activity_type, '', 'Canopy', 'Light', 'LUX', "{:3.1f}".format(lux), 'lux', 'TSL2561', status_qualifier,''])                        
            self._logger.debug("{}, {}, {:10.1f}".format("LUX", status_qualifier, lux))                                                                   
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            self._dbLogger.saveList([self._activity_type, '', 'Canopy', 'Light', 'LUX', '', 'lux', 'TSL2561', status_qualifier,str(e)])                                    
            self._logger.error("{}, {}, {}".format(name, status_qualifier, e))

    def getEC(self, test=False):
        """Record EC sensor (EC - ADC reading)
        Args:
            test: flag for testing
        Returns:
            None
        Raises:
            None
        """           

        from EC import EC
        self._logger.info("EC")

        try:
            s = EC()
            ec = s.getEC()
            
            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("EC", status_qualifier, ec))                
            self._dbLogger.saveList([self._activity_type, '', 'Reservoir', 'Nutrient', 'EC', "{:3.1f}".format(ec), 'EC', 'EC', status_qualifier,''])                                    
            self._logger.debug("{}, {}, {:10.1f}".format("EC", status_qualifier, ec))                                                                   
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("EC", status_qualifier, ec))
            self._dbLogger.saveList([self._activity_type, '', 'Reservoir', 'Nutrient', 'EC', '', 'EC', 'EC', status_qualifier,str(e)])                                                
            self._logger.error("{}, {}, {}".format("EC CCS811", status_qualifier, e))
            
    def getCO2_NDIR(self, test=False):
        """Record CO2 sensor (NDIR)
        Args:
            test: flag for testing
        Returns:
            None
        Raises:
            None
        """           
        from NDIR import NDIR
        self._logger.info("CO2 - NDIR")
        try:
            sensor = NDIR.Sensor()
            sensor.begin()
            co2=sensor.getCO2()

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("CO2 Canopy", status_qualifier, co2))                
            self._dbLogger.saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2', "{:3.1f}".format(co2), 'ppm', 'MH-Z16-NDIR', status_qualifier,''])                                                
            self._logger.debug("{}, {}, {:10.1f}".format("CO2", status_qualifier, co2))                                                       
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("CO2 Canopy", status_qualifier, co2))                                
            self._dbLogger.saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2', '', 'ppm', 'MH-Z16-NDIR', status_qualifier,str(e)])                                                            
            self._logger.error("{}, {}, {}".format("CO2 NDIR", status_qualifier, e))

    def getCO2_CCS811(self, test=False):
        """Record CO2 sensor (CCS811)
        Args:
            test: flag for testing
        Returns:
            None
        Raises:
            None
        """           
        from CCS811 import CCS811        
        self._logger.info("CO2 CCS811")
        try:
            sensor = CCS811(SLAVE)
            co2 = sensor.get_co2()

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("CO2 Canopy", status_qualifier, co2))                                
            self._dbLogger.saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2', "{:3.1f}".format(co2), 'ppm', 'CCS811', status_qualifier,''])                                                            
            self._logger.debug("{}, {}, {:10.1f}".format("CCS811 - CO2", status_qualifier, co2))                                                                                                  
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("CO2 Canopy", status_qualifier, co2))                                
            self._dbLogger.saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2','', 'ppm', 'CCS811', status_qualifier,str(e)])                                                                        
            self._logger.error("{}, {}, {}".format("CO2 CCS811", status_qualifier, e))
            
    def log(self, test=False):
        '''Log extra sensors
            Uncomment desired sensors
            Imports are in the function to avoid loading unnecessary code
        '''

        self.getOneWire(test)

        self.getLux(test)

        self.getEC(test)        

        #lg.getCO2_NDIR(test)

        #lg.getCO2_CCS811(test)
        
def main():
    '''
        Function that should get called from scripts
    '''
    lg = LogSensorExtra(Logger.INFO)
    lg.log()

def validate():
    '''
        Exercise the function to make sure it is working correctly
        Logs valid data
    '''
    lg = LogSensorExtra(Logger.DETAIL)
    lg.log()
    
def test():
    '''
        Use for debugging, outputs detail data
    '''
    test = True
    lg = LogSensorExtra(Logger.DETAIL)
    lg.log(test)

if __name__=="__main__":
    main()
