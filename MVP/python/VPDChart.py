'''

# Author: Howard Webb
# Data: 7/25/2017

# NOTE: this chart bins data into timestamp groups and uses multiple lines of data
# This is a test of combining temp, humidity and dewpoint

sudo pip install pandas
'''

import pygal
import requests
import json
from VaporPressure import main
import pandas as pd
import math
from datetime import datetime

#Use a view in CouchDB to get the data
#use the first key for attribute type
#order descending so when limit the results will get the latest at the top

def getResults(test=False):
    header={"Content-Type":"application/json"}
    ts = datetime.utcnow().isoformat()[:19]
    header={"Content-Type":"application/json"}       
    payload={"selector":{"start_date.timestamp":{"$lt":ts}, "status.status_qualifier":"Success", "activity_type":"Environment_Observation", "subject.name":"Air", "$or":[{"subject.attribute.name":"Humidity"}, {"subject.attribute.name":"Temperature"}]}, "fields":["start_date.timestamp", "subject.attribute.name", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":250}        
    url='http://localhost:5984/mvp_data/_find'
    if test:
        print(payload)
    return requests.post(url, json=payload, headers=header)    
 

def cleanData(data, test=False):
    '''Flatten structure to three columns'''
    out=[]
    for row in data.json()["docs"]:
#        print row
        hold={}
        # bin the timestamp into 20 minute groups
        d=datetime.strptime(row["start_date"]["timestamp"], '%Y-%m-%dT%H:%M:%S')
        d=d.replace(second=0, minute=int(math.floor(d.minute/20)))
        hold['timestamp']=str(d)
        hold["name"]=row["subject"]["attribute"]["name"]
        hold["value"]=row["subject"]["attribute"]["value"]
        out.append(hold)
    return out        

def buildChart(data, test=False):

    # Build dataframe from array
    df = pd.DataFrame.from_dict(data)
    df.set_index(['timestamp', 'name'])

    # Check for duplicates
    df = df.drop_duplicates(subset=['timestamp', 'name'])

    # Pivot the data by timestamp-bin with name groupings for columns
    df=df.pivot(index='timestamp', columns='name', values='value')
#    if test:
#        print(df)

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

# Calculate Vapor Pressure
    svp_a=[]
    avp_a = []
    vpd_a = []
    for idx, row in d1.iterrows():
#        print row
        svp, avp, vpd = main(float(row['Temperature']), float(row['Humidity']))        
        svp_a.append(float(svp))
        avp_a.append(float(avp))
        vpd_a.append(float(vpd))
    d1['SatVaporPressure']=svp_a
    d1['ActSatVaporPressure']=avp_a
    d1['VaporPressureDef']=vpd_a    

# Clear index so all are columns
    d3=d1.reset_index()
#    if test:
#        print(d3)

#build chart
    line_chart = pygal.Line()
    line_chart.title = 'Vapor Pressure Deficite'
    line_chart.y_title = "Pascals (newton/sq meter)"
    line_chart.y_title_secondary = "% or degree"

    line_chart.x_title="Timestamp (hover over to display date)"
    line_chart.x_labels = d3['timestamp']
    line_chart.add('Humidity', [float(row) for row in d3['Humidity']], secondary=True)
    line_chart.add('Temperature',[float(row) for row in d3['Temperature']], secondary=True)
    line_chart.add('Saturated',[float(row) for row in d3['SatVaporPressure']])
    line_chart.add('Actual',[float(row) for row in d3['ActSatVaporPressure']])
    line_chart.add('Deficit',[float(row) for row in d3['VaporPressureDef']])    
    filenm = '/home/pi/MVP/web/vpd_chart.svg'
    line_chart.render_to_file(filenm)
    if test:
        print("Render to " + filenm)

def getDewPointChart(test=False):
    data=getResults()
    data = cleanData(data)
    r_cnt=len(list(data))
    if r_cnt>0:
        print("Records: " + str(r_cnt))
        buildChart(data, test)
    else:
        print("No records selected")

def test():
    getDewPointChart(True)

if __name__=="__main__":
#    getDewPointChart()
   test()    
