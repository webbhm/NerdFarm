'''
Humidity Chart
# Author: Howard Webb
# Data: 5/6/2019
'''

from MultiChart import MultiChart

SUBJECT="Air"
ATTRIBUTE="Humidity"
FILE_NAME="/home/pi/MVP/web/humidity_chart.svg"
LABEL="Humidity"
UNITS="%"

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
