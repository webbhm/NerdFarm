'''
Log Optional sensors to CouchDB
Called from /home/pi/MVP/scripts/LogMVP.sh - needs to be uncommented for this to run
Uncomment desired functions in makeEnvObsv
Author: Howard Webb
Date: 5/3/2019
'''

from CouchUtil import saveList

class LogSensorExtra(object):

    def __init__(self):
        self._activity_type = "Environment_Observation"
        print("LogSensorsExtra")
        
    def getOneWire(self, test=False):
        from oneWireTemp import one_temp
        print("OneWire")
        for sensor in one_temp:
            if test:
                print(str(sensor), one_temp[sensor])
            self.logOneWire(sensor, one_temp[sensor], test)
            
    def logOneWire(self, sensor, name, test=False):
        '''Create json structure for temp'''
        from oneWireTemp import getTempC
        try:
            temp = getTempC(sensor)

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
            saveList([self._activity_type, '', name, 'Air', 'Temperature', "{:10.1f}".format(temp), 'Centigrade', 'DS18B20-' + str(sensor), status_qualifier,''])
            if test:
                print("{}, {}, {:10.1f}".format(name, status_qualifier, temp))
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format(name, status_qualifier, temp))
            saveList([self._activity_type, '', name, 'Air', 'Temperature', '', 'Centigrade', 'DS18B20-' + str(sensor), status_qualifier, str(e)])            
        
    def getLightCanopyLUXObsv(self, test=False):
        '''Create json structure for LUX'''
        from TSL2561 import TSL2561        
        lx = TSL2561()
        print("LUX")
        
        try:
            lux = lx.getLux()
            
            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("Lux", status_qualifier, lux))
                
            saveList([self._activity_type, '', 'Canopy', 'Light', 'LUX', "{:3.1f}".format(lux), 'lux', 'TSL2561', status_qualifier,''])                        
                               
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("Lux", status_qualifier, lux))                
            saveList([self._activity_type, '', 'Canopy', 'Light', 'LUX', '', 'lux', 'TSL2561', status_qualifier,str(e)])                                    
     

    def getNutrientReservoirECObsv(self, test=False):
        '''Create json structure for LUX'''
        from EC import EC
        print("EC")

        try:
            s = EC()
            ec = s.getEC()
            
            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("EC", status_qualifier, ec))                
            saveList([self._activity_type, '', 'Reservoir', 'Nutrient', 'EC', "{:3.1f}".format(ec), 'EC', 'EC', status_qualifier,''])                                    
                               
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("EC", status_qualifier, ec))
            saveList([self._activity_type, '', 'Reservoir', 'Nutrient', 'EC', '', 'EC', 'EC', status_qualifier,str(e)])                                                

    def getAirCanopyCO2Obsv(self, test=False):
        '''Create json structure for Canopy CO2'''
        from NDIR import NDIR
        print("CO2 - NDIR")
        try:
            sensor = NDIR.Sensor()
            sensor.begin()
            co2=sensor.getCO2()

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("CO2 Canopy", status_qualifier, co2))                
            saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2', "{:3.1f}".format(co2), 'ppm', 'MH-Z16-NDIR', status_qualifier,''])                                                
                               
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("CO2 Canopy", status_qualifier, co2))                                
            saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2', '', 'ppm', 'MH-Z16-NDIR', status_qualifier,str(e)])                                                            

    def getSecondCO2(self, test=False):
        '''Create json structure for LUX'''
        from CCS811 import CCS811        
        print("CO2 - CCS811")
        try:
            sensor = CCS811(SLAVE)
            co2 = sensor.get_co2()

            status_qualifier = 'Success'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("CO2 Canopy", status_qualifier, co2))                                
            saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2', "{:3.1f}".format(co2), 'ppm', 'CCS811', status_qualifier,''])                                                            
                               
        except Exception as e:
            status_qualifier = 'Failure'
            if test:
                status_qualifier = 'Test'
                print("{}, {}, {:10.1f}".format("CO2 Canopy", status_qualifier, co2))                                
            saveList([self._activity_type, '', 'Canopy', 'Air', 'CO2','', 'ppm', 'CCS811', status_qualifier,str(e)])                                                                        

    def makeEnvObsv(self, test=False):
        '''Log extra sensors
            Uncomment desired sensors
            Imports are in the function to avoid loading unnecessary code
        '''

        self.getOneWire(test)

        self.getLightCanopyLUXObsv(test)

        self.getNutrientReservoirECObsv(test)        

        #lg.getAirCanopyCO2Obsv(test)

        #lg.getSecondCO2(test)

if __name__=="__main__":
    '''Setup for calling from script'''
    lg = LogSensorExtra()                           
    lg.makeEnvObsv()

    

       
