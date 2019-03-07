# Author: Howard Webb
# Data: 7/25/2017

import pygal
import requests
import json
from datetime import datetime

def getResults(test=False):
    '''Run a Mango query to get the data'''
    ts = datetime.utcnow().isoformat()[:19]
    header={"Content-Type":"application/json"}   
    payload={"selector":{"start_date.timestamp":{"$lt":ts}, "status.status_qualifier":"Success", "activity_type":"Environment_Observation", "subject.name":"Nutrient","subject.location": "Reservoir","subject.attribute.name": "EC"}, "fields":["start_date.timestamp", "subject.attribute.value"], "sort":[{"start_date.timestamp":"desc"}], "limit":250}
    url='http://localhost:5984/mvp_data/_find'
#    if test:
#        print(payload)
    return requests.post(url, json=payload, headers=header)    

def buildChart(data, test=False):
    '''Build the chard from array data'''
    v_lst=[]
    ts_lst=[]
    for row in data.json()["docs"]:
        if test:
            print(row["start_date"]["timestamp"], row["subject"]["attribute"]["value"])
        v_lst.append(float(row["subject"]["attribute"]["value"]))
        ts_lst.append(row["start_date"]["timestamp"])
    if test:
        print(v_lst)
        print(ts_lst)

#    print(v_lst)
    #Build the chart from the lists
    line_chart = pygal.Line(range=(2000, 30000))
    line_chart.title = 'Electrical Conductivity'
    line_chart.y_title="ec"
    line_chart.x_title="Timestamp (hover over to display)"
    # reverse order for proper time sequence
    ts_lst.reverse()
    line_chart.x_labels = ts_lst

    #revrese order for proper time sequence
    v_lst.reverse()
    line_chart.add('EC', v_lst)
    fileNm='/home/pi/MVP/web/ec_chart.svg'
    if test:
        print("Rendering to file " + fileNm)
    #Save the chart as SVG to the web directory
    line_chart.render_to_file(fileNm)

def buildECChart(test=False):
    if test:
        print("Build EC Chart"    )
    data = getResults(test)
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
    buildECChart(True)

if __name__=="__main__":
    buildECChart()
#    test()


