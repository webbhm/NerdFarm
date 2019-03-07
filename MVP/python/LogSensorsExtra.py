#Log Test MVP sensors to CouchDB
from oneWireTemp import *
from TSL2561 import TSL2561
# from VL53L0X import *
from EC import EC
import NDIR
from CCS811 import CCS811, SLAVE
from CouchUtil import saveList
from LogUtil import get_logger

class LogSensorExtra(object):

    def __init__(self):
        self._logger = get_logger('LogSensorExtra')
        self._activity_type = "Environment_Observation"

    def getAirAmbientTempObsv(self, test=False):
        '''Create json structure for temp'''

        try:
            temp = getTempC(ambientTemp)

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Ambient', 'Air', 'Temperature', "{:10.1f}".format(temp), 'Farenheight', 'DS18B20_1', status_qualifier,''])
            self._logger.debug("{}, {}, {:10.1f}".format("Ambient Temp", status_qualifier, temp))            
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Ambient', 'Air', 'Temperature', '', 'Farenheight', 'DS18B20_1', status_qualifier, str(e)])            
            self._logger.error("{}, {}".format("Ambient Temp", e))            
        
    def getAirBoxTempObsv(self, test=False):
        '''Create json structure for temp'''
        try:
            temp = getTempC(boxTemp)

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Ambient', 'Air', 'Temperature', "{:10.1f}".format(temp), 'Farenheight', 'DS18B20_2', status_qualifier,''])            
            self._logger.debug("{}, {}, {:10.1f}".format("Box Air Temp", status_qualifier, temp))            

        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Ambient', 'Air', 'Temperature', '', 'Farenheight', 'DS18B20_2', status_qualifier, str(e)])                        
            self._logger.error("{}, {}".format("Box Air Temp", e))                                           
        
    def getAirTopTempObsv(self, test=False):
        '''Create json structure for temp'''
        try:
            temp = getTempC(topTemp)

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Top', 'Air', 'Temperature', "{:10.1f}".format(temp), 'Farenheight', 'DS18B20_3', status_qualifier,''])            
            self._logger.debug("{}, {}, {:10.1f}".format("Top Air Temp", status_qualifier, temp))
                               
                               
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Top', 'Air', 'Temperature', '', 'Farenheight', 'DS18B20_3', status_qualifier, str(e)])                                              
            self._logger.error("{}, {}".format("Top Air Temp", e))            
        
    def getNutrientReservoirTempObsv(self, test=False):
        '''Create json structure for temp'''
        try:
            temp = getTempC(reservoirTemp)

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Reservoir', 'Air', 'Temperature', "{:10.1f}".format(temp), 'Farenheight', 'DS18B20_4', status_qualifier,''])            
            self._logger.debug("{}, {}, {:10.1f}".format("Reservoir Temp", status_qualifier, temp))            
                               
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', 'Reservoir', 'Air', 'Temperature', '', 'Farenheight', 'DS18B20_4', status_qualifier, str(e)])                                                          
            self._logger.error("{}, {}".format("Reservoir Temp", e))
                               
    def getLightCanopyLUXObsv(self, test=False):
        '''Create json structure for LUX'''
        lx = TSL2561()
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
        '''Log all sensors'''

        self._logger.debug("{}".format("Ambient Air Temp"))            
        lg.getAirAmbientTempObsv(test)

        self._logger.debug("{}".format("Box Air Temp"))            
        lg.getAirBoxTempObsv(test)

        self._logger.debug("{}".format("Top Air Temp"))            
        lg.getAirTopTempObsv(test)

        self._logger.debug("{}".format("Reservoir Temp"))
        lg.getNutrientReservoirTempObsv(test)

        self._logger.debug("{}".format("Canopy LUX"))            
        lg.getLightCanopyLUXObsv(test)

        self._logger.debug("{}".format("Reservoir EC"))            
        lg.getNutrientReservoirECObsv(test)

        #self._logger.debug("{}".format("Canopy CO2"))            
        #lg.getAirCanopyCO2Obsv(test)

        self._logger.debug("{}".format("Alt CO2"))            
        lg.getSecondCO2(test)

        self._logger.debug("{}".format("EC"))            
        lg.getNutrientReservoirECObsv(test)

def test():
    lg = LogSensorExtra()                           
    lg.getNutrientReservoirECObsv()

if __name__=="__main__":
    '''Setup for calling from script'''
    lg = LogSensorExtra()                           
    lg.makeEnvObsv()
#    test()

    

       
