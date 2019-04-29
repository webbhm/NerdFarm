# Author: Howard Webb
# Data: 7/25/2017

# NOTE: this chart bins data into timestamp groups and uses multiple lines of data
# This is a test of combining temp, humidity and dewpoint

import pygal
import requests
import json
from DewPoint import getDewPoint
import pandas as pd
import math
from datetime import datetime
from MVP_Util import UTCStrToLDT

#Use a view in CouchDB to get the data
#use the first key for attribute type
#order descending so when limit the results will get the latest at the top

def getResults(test=False):
    '''Run a Mango query to get the data
           Args:
               Test:
           Returns:
               data array
           Raises:
               None
    '''

    ts = datetime.utcnow().isoformat()[:19]
    header={"Content-Type":"application/json"}    
    payload={"selector":{"start_date.timestamp":{"$lt":ts},"status.status_qualifier":{"$eq": "Success"}, "activity_type":{"$eq":"Environment_Observation"}, "subject.name":{"$eq": "Air"}, "$or":[{"subject.attribute.name":"Humidity"}, {"subject.attribute.name":"Temperature"}]}, "fields":["start_date.timestamp", "subject.attribute.name", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":250}        
    url='http://localhost:5984/mvp_data/_find'
    if test:
        print("Payload: " + str(payload))
        print("URL: " + url)
    return requests.post(url, json=payload, headers=header)


def cleanData(data, test=False):
    ''' Bin the timestamps into groups
        Pivot data into three groups (timestamp, temp, humidity)
           Args:
               data: array of values
               Test:
           Returns:
               None: cleaned array
           Raises:
               None
    '''
    
    out=[]
    print("Clean Data")
    print("Rows " + str(len(list(data))))
    for row in data.json()["docs"]:    
        hold={}
        # bin the timestamp into 20 minute groups
        # get only the first 19 characters of the timestamp
        d=UTCStrToLDT(row["start_date"]["timestamp"])
        d=d.replace(second=0, minute=int(math.floor(d.minute/20)))
        hold['timestamp']=str(d)
        hold["name"]=row["subject"]["attribute"]["name"]
        hold["value"]=row["subject"]["attribute"]["value"]
        out.append(hold)
    return out        

def buildChart(data, test=False):
    ''' Pivot and fill in array, then build the chart
           Args:
               data: array of values
               Test:
           Returns:
               None: (outputs chart file)
           Raises:
               None
    '''

    df = pd.DataFrame.from_dict(data)
    df.set_index(['timestamp', 'name'])

    # Check for duplicates
    df = df.drop_duplicates(subset=['timestamp', 'name'])

    # Pivot the data by timestamp-bin with name groupings for columns
    df=df.pivot(index='timestamp', columns='name', values='value')
    if test:
        print(df)
#    print df

# Fill missing data with dummy value
    df=df.fillna(11.1)

    #put in descending order
    d1=df.iloc[::-1]

#pull off only 120 rows
#    d1 = d1[:][:120]

# Reorder again
    d1=d1.iloc[::-1]

    # Make numeric (except for dates) - this does not seem to be working
    d1.apply(pd.to_numeric, errors='ignore')

#    print d1

# Calculate dew point
    dp=[]
    for idx, row in d1.iterrows():
#        print row
        dp.append(getDewPoint(float(row['Temperature']), float(row['Humidity'])))
    d1['Dewpoint']=dp

# Clear index so all are columns
    d3=d1.reset_index()

#build chart
    line_chart = pygal.Line(range=(0, 40))
    line_chart.title = 'Temperature,Humidity and Dew Point'
    line_chart.y_title="Degrees C"
    line_chart.x_title="Timestamp (hover over to display date)"
    line_chart.x_labels = d3['timestamp']
    line_chart.add('Humidity', [float(row) for row in d3['Humidity']], secondary=True)
    line_chart.add('Temperature',[float(row) for row in d3['Temperature']])
    line_chart.add('Dewpoint', d3['Dewpoint'])
    file_name = '/home/pi/MVP/web/dewpoint_chart.svg'    
    line_chart.render_to_file(file_name)
    if test:
        print("File: " + file_name)

def getDewPointChart(test=False):
    ''' Main chart builder coordinator
           Args:
               Test:
           Returns:
               None:
           Raises:
               None
    '''
    
    data = getResults(test)
    ls = list(data)
    r_cnt = len(ls)
    if r_cnt > 0:
        data2=cleanData(data, test)
        if test:
            print("Len Clean " + str(len(data2)))
        buildChart(data2, test)
    else:
        print("No Data")

if __name__=="__main__":
    getDewPointChart()
