'''
Log Optional sensors to CouchDB
Called from /home/pi/MVP/scripts/LogMVP.sh - needs to be uncommented for this to run
Uncomment desired functions in makeEnvObsv
Author: Howard Webb
Date: 5/3/2019
'''

from LogUtil import Logger
from Persistence import Persistence

class LogSensorsExtra(object):

    def __init__(self, lvl=Logger.INFO):
        """Record optional sensor data
        Args:
            lvl: Logging level
        Returns:
            None
        Raises:
            None
        """        
        self._logger = Logger("LogSensor-Extra", lvl, file="/home/pi/MVP/logs/obsv.log")
        self._activity_type = "Environment_Observation"
        self._test=False
        self._persist = Persistence(self._logger)
        
        
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
        self._logger.debug("In getOneWire")
        from OneWireTemp import OneWireTemp
        for sensor in OneWireTemp.one_temp:
            self.logOneWire(sensor, OneWireTemp.one_temp[sensor])
            
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
        self._logger.debug("In logOneWire")
        from OneWireTemp import OneWireTemp
        try:
            ow=OneWireTemp()
            temp = ow.getTempC(sensor)

            status_qualifier = 'Success'
            if self._test:
                status_qualifier = 'Test'
            rec = [self._activity_type, '', name, 'Air', 'Temperature', "{:10.1f}".format(temp), 'Centigrade', 'DS18B20-' + str(sensor), status_qualifier,'']
            self._persist.save(rec)
            self._logger.info("{}, {}, {:10.1f}".format(name, status_qualifier, temp))                                    
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            rec = [self._activity_type, '', name, 'Air', 'Temperature', '', 'Centigrade', 'DS18B20-' + str(sensor), status_qualifier, str(e)]                
            self._persist.save(rec)
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
            rec = [self._activity_type, '', 'Canopy', 'Light', 'LUX', "{:3.1f}".format(lux), 'lux', 'TSL2561', status_qualifier,'']
            self._persist.save(rec)
            self._logger.info("{}, {}, {:10.1f}".format("LUX", status_qualifier, lux))                                                                   
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            rec = [self._activity_type, '', 'Canopy', 'Light', 'LUX', '', 'lux', 'TSL2561', status_qualifier,str(e)]
            self._persist.save(rec)
            self._logger.error("{}, {}, {}".format("LUX", status_qualifier, e))

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
            rec = [self._activity_type, '', 'Reservoir', 'Nutrient', 'EC', "{:3.1f}".format(ec), 'EC', 'EC', status_qualifier,'']
            self._persist.save(rec)
            self._logger.info("{}, {}, {:10.1f}".format("EC", status_qualifier, ec))                                                                   
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("EC", status_qualifier, ec))
            rec = [self._activity_type, '', 'Reservoir', 'Nutrient', 'EC', '', 'EC', 'EC', status_qualifier,str(e)]
            self._persist.save(rec)            
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
        from NDIR import Sensor
        self._logger.info("CO2 - NDIR")
        try:
            sensor = Sensor()
            sensor.begin()
            co2=sensor.getCO2()

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("CO2 Canopy", status_qualifier, co2))                
            rec = [self._activity_type, '', 'Canopy', 'Air', 'CO2', "{:3.1f}".format(co2), 'ppm', 'MH-Z16-NDIR', status_qualifier,'']
            self._persist.save(rec)
            self._logger.debug("{}, {}, {:10.1f}".format("CO2", status_qualifier, co2))                                                       
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("CO2 Canopy", status_qualifier, co2))                                
            rec = [self._activity_type, '', 'Canopy', 'Air', 'CO2', '', 'ppm', 'MH-Z16-NDIR', status_qualifier,str(e)]
            self._persist.save(rec)
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
            rec = [self._activity_type, '', 'Canopy', 'Air', 'CO2', "{:3.1f}".format(co2), 'ppm', 'CCS811', str(e)]
            self._persist.save(rec)
            self._logger.debug("{}, {}, {:10.1f}".format("CCS811 - CO2", status_qualifier, co2))                                                                                                  
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("CO2 Canopy", status_qualifier, co2))                                
            rec = [self._activity_type, '', 'Canopy', 'Air', 'CO2','', 'ppm', 'CCS811', status_qualifier,str(e)]
            self._persist.save(rec)
            self._logger.error("{}, {}, {}".format("CO2 CCS811", status_qualifier, e))
            
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
            c_rec = ['Environment_Observation', '', 'Top', 'Air', 'CO2', "{:10.1f}".format(co2), 'ppm', 'scd30', status, '']
            t_rec = ['Environment_Observation', '', 'Top', 'Air', 'Temperature', "{:10.1f}".format(temp), 'Centigrade', 'scd30', status, '']
            h_rec = ['Environment_Observation', '', 'Top', 'Air', 'Humidity', "{:10.1f}".format(rh), 'Percent', 'scd30', status, '']            
            self._persist.save(c_rec)
            self._persist.save(t_rec)
            self._persist.save(h_rec)            
            self._logger.info("{} {:6.1f}, {} {:3.1f}, {} {:3.1f}".format("EnvObsv-CO2:", co2, "Temp", temp, "Humidity:", rh))            
        except Exception as e:
            status = 'Failure'
            if self._test:
                status = 'Test'
            c_rec = ['Environment_Observation', '', 'Top', 'Air', 'CO2', '', 'ppm', 'scd30', status, str(e)]
            t_rec = ['Environment_Observation', '', 'Top', 'Air', 'Temperature', '', 'Centigrde', 'scd30', status, '']
            h_rec = ['Environment_Observation', '', 'Top', 'Air', 'Humidity', '', 'Percent', 'scd30', status, '']
            self._persist.save(c_rec)
            self._persist.save(t_rec)
            self._persist.save(h_rec)            
            self._logger.debug("{} {}".format("EnvObsv-SCD30 Error:", e))            
            
    def log(self):
        '''Log extra sensors
            Uncomment desired sensors
            Imports are in the function to avoid loading unnecessary code
        '''

        #self.getOneWire()

        self.getLux()

        self.getEC()        

        self.getCO2_NDIR()

        #self.getCO2_CCS811()
        
        self.getSCD()
        
        
def test():
    '''
        Use for debugging, outputs detail data
    '''    
    print("Testing SDC30")
    ls = LogSensorsExtra()
    ls._logger.setLevel(Logger.DEBUG)
    ls._test = True
    ls.log()
    
def validate():
    '''
        Exercise the function to make sure it is working correctly
        Logs valid data
    '''    
    print("Validate SDC30")    
    main(Logger.INFO)
    
def main(level=Logger.INFO):
    '''
        Function that should get called from scripts
    '''    
    ls = LogSensorsExtra()
    ls._logger.setLevel(level)
    ls.log()

if __name__=="__main__":
    main()    
