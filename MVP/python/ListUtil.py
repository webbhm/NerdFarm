'''
Utility to take a sensor record and turn it into a list for Google Sheets
Author: Howard Webb
Date: 11/22/2019
'''

from datetime import datetime
from datetime import timedelta
from env import env
import math
from LogUtil import Logger

NBR_PLANTS = 6
TS = 0
FIELD = 1
ACTIVITY = 2
TRIAL = 3
PLOT = 4
SUBJECT = 5
ATTRIBUTE = 6
VALUE = 7
UNITS = 8
PARTICIPANT = 9
STATUS = 10
COMMENT = 11
class ListUtil(object):
    
    def __init__(self, logger=None):
        if logger == None:
            self._logger = Logger("ListUtil", Logger.DETAIL)
        else:
            self._logger = logger
        self._logger.detail("Initialize ListUtil")
    

    def build(self, doc):
        '''
        Convert activity list to list of lists
        Args:
            doc: list of attributes, should be of format:
                 [activity_name, trial, plot, subject, attribute, value, units, participant, status_qualifier, comment]
                 participant may be a device string, or a list: ['person':'hmw']
        Returns:
            rec: list formatted record ready for the spreadsheet
        Throws:
            None

        '''
        # add timestamp and field_id
        timestamp = datetime.utcnow()
        ts_str = timestamp.isoformat()[:19]
        t_str = ts_str.replace('T', ' ')
        doc.insert(0, env['field']['field_id'])
        doc.insert(0, t_str)
        
        # append date, week of trial
        start = env['trials'][0]['start_date']
        st = datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        dif = timestamp - st
        # Week of trial
        wk = int(math.ceil(dif.days/7))
        # date portion
        doc.append(t_str[:10])
        # time portion        
        doc.append(t_str[-8:])
        # weeks of trial
        doc.append(wk)
        # create binned timestamp - time is 20 minute group
        ts2=timestamp.replace(minute=(int(math.floor(timestamp.minute/20))), second=0)
        ts2_str = ts2.isoformat()[:19]
        doc.append(ts2_str)
        # fix participant
        if isinstance(doc[PARTICIPANT], list):
            p_type = doc[PARTICIPANT][0]
            p_name = doc[PARTICIPANT][1]
            del doc[PARTICIPANT]
            doc.insert(PARTICIPANT, p_name)
            doc.insert(PARTICIPANT, p_type)
        else:
            doc.insert(PARTICIPANT, 'device')
        # Remove 'Field' from Environment & State
        # 'Plot' is used for Location of sensor
        self._logger.debug(doc[2])
        if doc[2] == 'Environment_Observation':
            del doc[3]
        if doc[2] == 'State_Change':
            del doc[3]
        # convert to list of lists
        doc2 = [[el] for el in doc]
        self._logger.debug(doc2)
        return doc2

def test(level=Logger.DEBUG):
    print("ListUtil Test")
    util = ListUtil()
    util._logger.setLevel(level)
    from TestRecords import recs
    for rec in recs:
        util.build(rec)
    print("Done")      
    
if __name__=="__main__":
    test()
