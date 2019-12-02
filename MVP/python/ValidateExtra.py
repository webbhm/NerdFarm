'''
Validation routine to check code on optional items
Author: Howard Webb
Date: 5/7/2019
'''
from LogUtil import Logger

class ValidateExtra(object):
    
    def __init__(self):
        """Record optional sensor data
        Args:
            lvl: Logging level
        Returns:
            None
        Raises:
            None
        """
        self._logger=Logger("ValidateExtra")

    def validate(self):
        print("Validate Code")
        self.validateSensors()
        self.validateActuators()
        self.validateControllers()
        
    def validateSensors(self):
        print("Validate Sensors")
        print("Validate Sensor Logging")
        from LogSensorsExtra import validate as se_valid
        se_valid()

    def validateActuators(self):
        print("\nValidate Actuators")
        print("Validate Pump")
        from Reservoir import validate as r_valid
        r_valid()
        from Fan import validate as f_valid
        f_valid()

    def validateControllers(self):
        print("\nValidate Controllers")
        print("\nValidate Persistanace")
        from Persistence import validate as per_val
        per_val()
        from Thermostat import validte as t_valid
        t_valid()
        
def main():
    v = ValidateExtra()
    v.validate()
    

if __name__=="__main__":
    main()    
        
