'''
Router for persisting records
There is not much to this object, but is separates the sensors and actuators
  from the mechanics of storing record data.
This is where changes may be made for different persistent platforms
Currently only CouchDB is implemented
  CouchDB
  Google Sheets
  CSV files
  MQTT
Lower level utilities format the record and handle the hardware issues
Author: Howard Webb
Date: 11/22/2019
'''
from datetime import datetime
from datetime import timedelta
from env import env
from LogUtil import Logger
from CouchUtil import CouchUtil
#from G_AppendUtil import AppendUtil


class Persistence(object):
    
    def __init__(self, logger=None):
        if logger == None:
            self._logger = Logger("Persistence", Logger.DETAIL)
        else:
            self._logger = logger
        self._activity_type = "Environment_Observation"
        self._couch = CouchUtil(self._logger)
        #self._sheet = AppendUtil(self._logger)
        self._test = False
        self._logger.detail("Initialized Persistence")        
     
    def save(self, doc, test=False):
        '''
        Args:
            doc: list of attributes, should be of format:
                 [activity_name, trial, plot, subject, attribute, value, units, participant, status_qualifier, comment]
                 participant may be a device string, or a list: ['person':'hmw']
        Returns:
            None
        Throws:
            None

        '''
        self._logger.detail("In saveRecord")        
        # Add a line for each persistence service to be used
        # be sure to copy the record so formatting from one
        #  does not impact another system
        self._couch.save(doc.copy())
        #self._sheet.save(doc.copy())
        
def validate():
    test(Logger.INFO)
    
def test(level=Logger.DEBUG):    
    print("Persistence Test")
    util = Persistence()
    util._logger.setLevel(level)
    from TestRecords import recs
    for rec in recs:
        util.save(rec)
    print("Done")
    
if __name__=="__main__":
    test()
        
