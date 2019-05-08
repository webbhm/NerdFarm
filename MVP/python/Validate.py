'''
Validation routine to check code
Author: Howard Webb
Date: 5/7/2019
'''
from LogUtil import Logger

class Validate(object):
    
    def __init__(self):
        """Record optional sensor data
        Args:
            lvl: Logging level
        Returns:
            None
        Raises:
            None
        """
        self._logger=Logger("Validate")

    def validate(self):
        print("Validate Code")
        self.validateSensors()
        self.validateActuators()
        self.validateControllers()
        
    def validateSensors(self):
        print("Validate Sensors")
        print("\nValidate SI7021")
        from SI7021 import validate as si_val
        si_val()

    def validateActuators(self):
        print("\nValidate Actuators")
        print("\nValidate Fan")
        from Fan import validate as f_val
        f_val()
        print("\nValidate Lights")
        from Light import validate as l_val
        l_val()

    def validateControllers(self):
        print("\nValidate Controllers")
        print("\nValidate Thermostat")
        from Thermostat import validate as therm_val
        therm_val()
        
def main():
    v = Validate()
    v.validate()
    

if __name__=="__main__":
    main()    
        