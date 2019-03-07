# Author: Howard Webb
# Data: 7/25/2017

import pygal
import requests
import json
from datetime import datetime


def getResults(test=False):
    if test:
        print("Get LUX results")
    '''Run a Mango query to get the data'''
    ts = datetime.utcnow().isoformat()[:19]    
#    payload={"selector":{"start_date.timestamp":{"$lt":ts}, "status.status_qualifier":"Success", "activity_type":"Environment_Observation", "subject.name":"Light"}, "fields":["start_date.timestamp", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":250}
    payload={"selector":{"start_date.timestamp":{"$lt":ts}, "status.status_qualifier":"Success", "activity_type":"Environment_Observation", "subject.name":"Light","subject.attribute.name": "LUX"}, "fields":["start_date.timestamp", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":250}
    header={"Content-Type":"application/json"}    
    url='http://localhost:5984/mvp_data/_find'
#    if test:
#        print(payload)
    return requests.post(url, json=payload, headers=header)
    
def buildChart(data, test=False):
    if test:
        print("Build Chart")
    '''Build the chard from array data'''
    v_lst=[]
    ts_lst=[]
    for row in data.json()["docs"]:
        v_lst.append(float(row["subject"]["attribute"]["value"]))
        ts_lst.append(row["start_date"]["timestamp"])
        if test:
            print(str(row["start_date"]["timestamp"]) + " " + str(row["subject"]["attribute"]["value"]))
    #Build the chart from the lists
    line_chart = pygal.Line(range=(0, 20000))
    line_chart.title = 'LUX'
    line_chart.y_title="lux"
    line_chart.x_title="Timestamp (hover over to display)"
    # reverse order for proper time sequence
    ts_lst.reverse()
    line_chart.x_labels = ts_lst

    #revrese order for proper time sequence
    v_lst.reverse()
    line_chart.add('LUX', v_lst)

    #Save the chart as SVG to the web directory
    dir='/home/pi/MVP/web/lux_chart.svg'
    line_chart.render_to_file(dir)
    if test:
        print("Lux saved to : " + dir)

def buildLuxChart(test=False):
    if test:
        print("Build LUX Chart")
    data=getResults(test)
    if data.status_code == 200:
        r_cnt=len(data.json()["docs"])    
        if r_cnt>0:
            print("Records: ", r_cnt)
            buildChart(data, test)
        else:
            print("No records selected " + r_cnt)
            print(data.reason)
    else:
        print("No Data, Reason: " + data.reason)


def test():
    buildLuxChart(True)

if __name__=="__main__":
    buildLuxChart()

