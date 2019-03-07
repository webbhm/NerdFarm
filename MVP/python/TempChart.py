'''
# Author: Howard Webb
# Data: 7/25/2017
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

#Use a view in CouchDB to get the data
#use the first key for attribute type
#order descending so when limit the results will get the latest at the top

ATTRIBUTE="Temperature"

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
    payload={"selector":{"start_date.timestamp":{"$lt":ts}, "status.status_qualifier":"Success", "activity_type":"Environment_Observation","subject.name":"Air","subject.attribute.name":ATTRIBUTE}, "fields":["start_date.timestamp", "participant.name", "subject.location", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":250}
    url='http://localhost:5984/mvp_data/_find'
    if test:
        print("Payload: " + str(payload))
        print("URL: " + url)
    return requests.post(url, json=payload, headers=header)
    
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
#    print(df)

    # Check for duplicates
    #print(df.duplicated(subset=['timestamp', 'name']))
    df = df.drop_duplicates(subset=['timestamp', 'name'])

    # Pivot the data by timestamp-bin with name groupings for columns
    df=df.pivot(index='timestamp', columns='name', values='value')
    if test:
        print(df)
        for nm in df.columns:
            print("Name: " + nm)
        print("Columns: " + df.columns)

# Fill missing data with dummy value
    df=df.fillna(20.0)

    #put in descending order
    d1=df.iloc[::-1]

    d2=d1.to_records()
#    print(d2)

    # Create the chart
    #build chart
    #line_chart = pygal.Line(range=(350, 2000))
    line_chart = pygal.Line()    
    line_chart.title = ATTRIBUTE
    line_chart.y_title="Degree C"
    line_chart.x_title="Timestamp (hover over to display date)"
    
    # Pull the values from the rows and build a list
    l=len(d2[0])
    if test:
        print("Len: " + str(l))
    # Values for chart range
    mx = 0  # maximum value
    mn = 5000  # minimum value
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
            mx2 = max(dta[ix])
            mn2 = min(dta[ix])
            if mx2 > mx:
                mx = mx2
            if mn2 < mn:
                mn = mn2

        # reverse the value order
        dta[ix].reverse()
        # add chart line for each data value
        if ix > 0:
            # Add column name and data
            line_chart.add(df.columns[ix-1], dta[ix])            
            if test:
                print("Label: " + str(df.columns[ix-1]))
                #print(str(dta[ix]))
    # set min/max scale
    chart_name = '/home/pi/MVP/web/temp_chart.svg'
    line_chart.render_to_file(chart_name)
    if test:
        print("Chart: " + chart_name)


def buildMultiChart(test=False):
    ''' Main chart builder coordinator
           Args:
               Test:
           Returns:
               None:
           Raises:
               None
    '''

    data=getResults(test)
    # process if no errors
    if data.status_code == 200:
        r_cnt= len(data.json()["docs"])
        if r_cnt>0:
            if test:
                print("Records: " +str(r_cnt))
            d2=cleanDate(data, test)
            buildChart(d2, test)
        else:
            print("No records selected")
    else:
        print("No Data, Reason: " + str(data.reason))

def cleanDate(data, test=False):
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

def test():
    ''' Function to test the chart building with test flag set to True
           Args:
               None:
           Returns:
               None:
           Raises:
               None
    '''
    buildMultiChart(True)
        

if __name__=="__main__":
    buildMultiChart()
