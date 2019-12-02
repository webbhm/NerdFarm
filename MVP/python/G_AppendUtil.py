'''
High level handler for Google Sheet persistence
1) Formats it into a list of lists
2) Persists it to a sheet
Author: Howard Webb
Date: 11/22/2019
'''
from ListUtil import ListUtil
from SheetUtil import SheetUtil
from LogUtil import Logger


class AppendUtil(object):
    
    def __init__(self, logger=None):
        """Record optional sensor data
        Args:
            lvl: Logging level
        Returns:
            None
        Raises:
            None
        """            
        if logger == None:
            self._logger = Logger("AppendUtil", Logger.DETAIL)
        else:
            self._logger = logger
        self._sheet_name = '1Mtlr_-yqwdEwXFEcaLoEP01aDN7vvOosDOEerFpDkaI'
        self._scope = ['https://www.googleapis.com/auth/spreadsheets']
        self._l_util = ListUtil(self._logger)
        self._s_util = SheetUtil(self._sheet_name, self._scope, self._logger)
        self._logger.debug("Initialized AppendUtil")
        
    def append(self, rec, append_range):
        #print(rec)
        self._s_util.append(append_range, rec)
        
    def save(self, doc):
        '''
        This is the entry function into the object
        Lookup the range in the dictionary before appending
        Save list to Google Sheet
        Args:
            self
            doc - formatted list to save (append)
        Returns:
            None
        Throws:
            None

        '''
        self._logger.detail("In save")
        name = doc[0]
        self._logger.debug('%s: %s' % ('Rec Type', name))
        rec = self._l_util.build(doc)
        # dictionary of sheet tabs
        range = {'Environment_Observation':'Environment!A1', 'State_Change':'State!A1', 'Agronomic_Activity':'Agronomic!A1', 'Phenotype_Observation':'Phenotype!A1'}
        # Lookup range for record type - note this is a lookup on a list of lists
        
        append_range = range[name]
        self._logger.debug('%s: %s' % ('Range', append_range))
        self._s_util.append(append_range, rec)

def test2():
    print("AppendUtil Test")
    util = AppendUtil()
    from RecordTester import RecordTester
    rt = RecordTester()
    rt.test(util.save)
    print("Done")
    
def test():
    print("AppendUtil Test")
    util = AppendUtil()
    from TestRecords import recs
    for rec in recs:
        util.save(rec)
    print("Done")    
    
if __name__=="__main__":
    test()
