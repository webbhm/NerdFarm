# Temperature chart with data from CouchDB
# Author: Howard Webb
# Date: 3/5/2018

import pygal
import requests
import json
from datetime import datetime

#Use a view in CouchDB to get the data
#use the first key for attribute type
#order descending so when limit the results will get the latest at the top

def getResults(test=False):
    '''Run a Mango query to get the data'''
    ts = datetime.utcnow().isoformat()[:19]
    header={"Content-Type":"application/json"}    
    payload={"selector":{"start_date.timestamp":{"$lt":ts}, "status.status_qualifier":"Success", "activity_type":"Environment_Observation", "subject.name":"Air","subject.attribute.name": "Humidity"}, "fields":["start_date.timestamp", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":250}
    url='http://localhost:5984/mvp_data/_find'
    if test:
        print("Payload: " + str(payload))
        print("URL: " + url)
    return requests.post(url, json=payload, headers=header)
    
   
def buildChart(data, test=False):
    '''Build the chard from array data'''
    v_lst=[]
    ts_lst=[]
    for row in data.json()["docs"]:    
    #for row in data:
        if test:
            print(row)
        v_lst.append(float(row["subject"]["attribute"]["value"]))
        ts_lst.append(row["start_date"]["timestamp"])


    line_chart = pygal.Line()
    line_chart.title = 'Humidity'
    line_chart.y_title="Percent"
    line_chart.x_title="Timestamp (hover over to display date)"
    #need to reverse order to go from earliest to latest
    ts_lst.reverse()
    line_chart.x_labels = ts_lst
    #need to reverse order to go from earliest to latest
    v_lst.reverse()
    line_chart.add('Humidity', v_lst)
    file_name = '/home/pi/MVP/web/humidity_chart.svg'    
    line_chart.render_to_file(file_name)
    if test:
        print("File: " + file_name)

def buildTempChart(test=False):
    data=getResults(test)
    r_cnt=len(list(data))    
    if r_cnt>0:
        print("Records: " + str(r_cnt))
        buildChart(data, test)
    else:
        print("No records selected")

def test():
    buildTempChart(True)
    
if __name__=="__main__":
    buildTempChart(True)

