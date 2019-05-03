'''
Log Optional sensors to CouchDB
Called from /home/pi/MVP/scripts/LogMVP.sh - needs to be uncommented for this to run
Uncomment desired functions in makeEnvObsv
Author: Howard Webb
Date: 5/3/2019
'''

from CouchUtil import saveList
from LogUtil import get_logger

class LogSensorExtra(object):

    def __init__(self):
        self._logger = get_logger('LogSensorExtra')
        self._activity_type = "Environment_Observation"
        
    def getOneWire(self, test=False):
        from oneWireTemp import one_temp     
        for sensor in one_temp:
            if test:
                print(str(sensor), one_temp[sensor])
            self.logOneWire(sensor, one_temp[1], test)
            
            
    def logOneWire(self, sensor, name, test=False):
        '''Create json structure for temp'''
        from oneWireTemp import getTempC
        try:
            temp = getTempC(sensor)

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', name, 'Air', 'Temperature', "{:10.1f}".format(temp), 'Farenheight', 'DS18B20-' + str(sensor), status_qualifier,''])
            self._logger.debug("{}, {}, {:10.1f}".format("Ambient Temp", status_qualifier, temp))            
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', name, 'Air', 'Temperature', '', 'Farenheight', 'DS18B20-' + str(sensor), status_qualifier, str(e)])            
            self._logger.error("{}, {}".format("Ambient Temp", e))            
        
                               
    def getLightCanopyLUXObsv(self, test=False):
        '''Create json structure for LUX'''
        from TSL2561 import TSL2561        
        lx = TSL2561()

        self._logger.debug("{}".format("Canopy LUX"))            
        
        try:
            lux = lx.getLux()
            
            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Canopy', 'Light', 'LUX', "{:3.1f}".format(lux), 'lux', 'TSL2561', status_qualifier,''])                        
            self._logger.debug("{}, {}, {:10.1f}".format("Canopy LUX", status_qualifier, lux))            
                               
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Canopy', 'Light', 'LUX', '', 'lux', 'TSL2561', status_qualifier,str(e)])                                    
            self._logger.error("{}, {}".format("Canopy LUX", e))                                           
     

    def getNutrientReservoirECObsv(self, test=False):
        '''Create json structure for LUX'''
        from EC import EC

        self._logger.debug("{}".format("Reservoir EC"))

        try:
            s = EC()
            ec = s.getEC()
            
            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Reservoir', 'Nutrient', 'EC', "{:3.1f}".format(ec), 'EC', 'EC', status_qualifier,''])                                    
            self._logger.debug("{}, {}, {:10.1f}".format("Reservoir EC", status_qualifier, ec))            
                               
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Reservoir', 'Nutrient', 'EC', '', 'EC', 'EC', status_qualifier,str(e)])                                                
            self._logger.error("{}, {}".format("Reservoir Depth", e))                                           

    def getAirCanopyCO2Obsv(self, test=False):
        '''Create json structure for Canopy CO2'''
        from NDIR import NDIR
        self._logger.debug("{}".format("Canopy CO2"))
        
        try:
            sensor = NDIR.Sensor()
            sensor.begin()
            co2=sensor.getCO2()

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2', "{:3.1f}".format(co2), 'ppm', 'MH-Z16-NDIR', status_qualifier,''])                                                
            self._logger.debug("{}, {}, {:10.1f}".format("Canopy CO2", status_qualifier, co2))            
                               
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2', '', 'ppm', 'MH-Z16-NDIR', status_qualifier,str(e)])                                                            
            self._logger.error("{}, {}".format("Canopy CO2", e))                                           

    def getSecondCO2(self, test=False):
        '''Create json structure for LUX'''
        from CCS811 import CCS811        
        self._logger.debug("{}".format("Alt CO2"))
        
        try:
            sensor = CCS811(SLAVE)
            co2 = sensor.get_co2()

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2', "{:3.1f}".format(co2), 'ppm', 'CCS811', status_qualifier,''])                                                            
            self._logger.debug("{}, {}, {:10.1f}".format("Alt CO2", status_qualifier, co2))            
                               
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2','', 'ppm', 'CCS811', status_qualifier,str(e)])                                                                        
            self._logger.error("{}, {}".format("Alt CO2", e) )                                          


    def makeEnvObsv(self, test=False):
        '''Log extra sensors
            Uncomment desired sensors
            Imports are in the function to avoid loading unnecessary code
        '''

        self.getOneWire(True)

        self.getLightCanopyLUXObsv(test)

        self.getNutrientReservoirECObsv(test)        

        #lg.getAirCanopyCO2Obsv(test)

        #lg.getSecondCO2(test)

if __name__=="__main__":
    '''Setup for calling from script'''
    lg = LogSensorExtra()                           
    lg.makeEnvObsv()

    

       
