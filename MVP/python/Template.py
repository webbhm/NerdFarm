"""
This is not working code.
This is a template showing the programming patterns.
Replace "Template" with your name and add new functionality

 Author : Howard Webb
 Date   : 06/20/2018
 
"""

# imports of shared code
from LogUtil import Logger
import time

# declaration of class object
class Template(object):

   def __init__(self, logger=None):
      """Initialize the object
           Args:
               logger: existing logger to use
           Returns:
               rh: calculated relative humidity
           Raises:
               None
      """
      if logger == None:
          self._logger = Logger("Template", Logger.INFO, "/home/pi/MVP/logs/template.log")
          
    def doSomething(self):
      """Function to do something
           Args:
               none:
           Returns:
               thing:
           Raises:
               None
      """
        self._logger.debug("In doSomething")
        thing = True
        self._logger.debug("{}: {}".format("thing", thing))
        return thing
    
def test():
    """Development and debugging activity
        Add detail tests here
        Args:
            None
        Returns:
            None
        Raises:
            None
    """
    t=Template()
    print("Test Template")
    while True:
       thing = t.doSomething()
       si._logger.info("{}: {}".format("Something", thing))
       time.sleep(10)
       
def validate(level=Logger.INFO):
    """Quick test that things are working
        Args:
            None
        Returns:
            None
        Raises:
            None
   """
    print("Validate Template")
    thing = Thing()
    thing._logger.setLevel(level)
    thng = thing.doSomething()        
    if thng != None:
        print("{}: {}".format("Thing", thng))
    else:
        print("Error getting Thing")
        
def main():
    pass
    
if __name__ == "__main__":
    test()
