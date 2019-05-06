'''
# Author: Howard Webb
# Data: 7/25/2017
  Generic charter that handles multiple sensor input
  This should never be run stand-alone
# NOTE: this chart bins data into timestamp groups and uses multiple lines of data
  The chart can handle single or multiple data sets (ie sensors)
'''

import pygal
import requests
# python3 -m pip install --user numpy pandas
import pandas as pd
import json
from datetime import datetime, time
import math
from LogUtil import Logger

#Use a view in CouchDB to get the data
#use the first key for attribute type
#order descending so when limit the results will get the latest at the top

class MultiChart(object):
    
    DETAIL = Logger.DETAIL
    DEBUG = Logger.DEBUG    
    INFO = Logger.INFO
    ERROR = Logger.ERROR
    
    def __init__(self, subject, attribute, label, units, file_name):
    
      self._subject = subject
      self._attribute = attribute
      self._label = label
      self._units = units
      self._file_name = file_name
      self._logger = Logger(self._attribute + "Chart", Logger.INFO)
 
    def setLevel(self, level):
        '''Set logging level
               Args:
                   level: logging level
               Returns:
                   None
               Raises:
                   None
        '''
        self._logger.detail("In setLevel")
        self._logger.setLevel(level)

    def getResults(self):
        '''Run a Mango query to get the data
               Args:
                   Test:
               Returns:
                   data array
               Raises:
                   None
        '''
        self._logger.detail("In getResults")
        ts = datetime.utcnow().isoformat()[:19]
        header={"Content-Type":"application/json"}
        payload={"selector":{"start_date.timestamp":{"$lt":ts}, "status.status_qualifier":"Success", "activity_type":"Environment_Observation","subject.name":self._subject,"subject.attribute.name":self._attribute}, "fields":["start_date.timestamp", "participant.name", "subject.location", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":250}
        url='http://localhost:5984/mvp_data/_find'
        self._logger.debug("URL: " + url)
        self._logger.debug("Payload: " + str(payload))

        return requests.post(url, json=payload, headers=header)
        
    def buildChart(self, data):    
        ''' Pivot and fill in array, then build the chart
               Args:
                   data: array of values
                   Test:
               Returns:
                   None: (outputs chart file)
               Raises:
                   None
        '''
        self._logger.detail("In buildChart")
        df = pd.DataFrame.from_dict(data)
        df.set_index(['timestamp', 'name'])
        self._logger.detail(df)

        # Check for duplicates
        #print(df.duplicated(subset=['timestamp', 'name']))
        df = df.drop_duplicates(subset=['timestamp', 'name'])

        # Pivot the data by timestamp-bin with name groupings for columns
        df=df.pivot(index='timestamp', columns='name', values='value')
        for nm in df.columns:
            self._logger.detail("Name: " + nm)
            self._logger.detail("Columns: " + df.columns)

    # Fill missing data with dummy value
        df=df.fillna(20.0)

        #put in descending order
        d1=df.iloc[::-1]

        d2=d1.to_records()
        self._logger.detail(d2)

        # Create the chart
        #build chart
        #line_chart = pygal.Line(range=(350, 2000))
        line_chart = pygal.Line()    
        line_chart.title = ATTRIBUTE
        line_chart.y_title=UNITS
        line_chart.x_title="Timestamp (hover over to display date)"
        
        # Pull the values from the rows and build a list
        l=len(d2[0])
        self._logger.detail("Len: " + str(l))
        # holder for data outputs    
        dta = []
        # Loop all data sets
        for x in range(0, l):
            ix = int(x)
            if x == 0:
                # timestamp
                dta.insert(ix, [row[int(x)] for row in d2])
                line_chart.x_labels = dta[ix]
            else:
                # values
                dta.insert(ix, [float(row[ix]) for row in d2])

            # reverse the value order
            dta[ix].reverse()
            # add chart line for each data value
            if ix > 0:
                # Add column name and data
                line_chart.add(df.columns[ix-1], dta[ix])            
                self._logger.detail("Label: " + str(df.columns[ix-1]))
                    #print(str(dta[ix]))
        # set min/max scale
        line_chart.render_to_file(self._file_name)


    def buildMultiChart(self):
        ''' Main chart builder coordinator
               Args:
                   Test:
               Returns:
                   None:
               Raises:
                   None
        '''
        self._logger.detail("In buildMultiChart")
        data=self.getResults()
        # process if no errors
        if data.status_code == 200:
            r_cnt= len(data.json()["docs"])
            if r_cnt>0:
                self._logger.detail("Records: " +str(r_cnt))
                d2=self.cleanDate(data)
                self.buildChart(d2)
                self._logger.info(self._attribute + " chart created, records: " + str(r_cnt) + " to " + self._file_name)
            else:
                self._logger.error("No records selected")
        else:
            self._logger.error("No Data, Reason: " + str(data.reason))

    def cleanDate(self, data):
        ''' Bin the timestamps into groups
               Args:
                   data: array of values
                   Test:
               Returns:
                   None: cleaned array
               Raises:
                   None
        '''
        
        d2=[]
        for row in data.json()["docs"]:
            rw={}
            ts=datetime.strptime(row["start_date"]["timestamp"], '%Y-%m-%dT%H:%M:%S')
            # create data bins
            ts2=ts.replace(minute=(int(math.floor(ts.minute/20))), second=0)
            # replace timestamp with bined data
            # Array indexes must match query references
            rw["timestamp"]=str('{:%Y-%m-%d %H:%M:%S}'.format(ts2))
            rw["name"]=row["participant"]["name"]+"-"+row["subject"]["location"]
            rw["value"]=row["subject"]["attribute"]["value"]
            d2.append(rw)
        return d2
    
SUBJECT="Air"
ATTRIBUTE="Temperature"
FILE_NAME="/home/pi/MVP/web/temp_chart.svg"
LABEL="Temperature"
UNITS="Degree C"

def test():
    ''' Function to test the chart building with test flag set to True
           Args:
               None:
           Returns:
               None:
           Raises:
               None
    '''
    chart = MultiChart(SUBJECT, ATTRIBUTE, LABEL, UNITS, FILE_NAME)
    chart.setLevel(chart.DEBUG)
    chart.buildMultiChart()
    
def validate():    
    chart = MultiChart(SUBJECT, ATTRIBUTE, LABEL, UNITS, FILE_NAME)
    chart.setLevel(chart.INFO)
    chart.buildMultiChart()
        

if __name__=="__main__":
    validate()

