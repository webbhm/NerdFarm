'''
Temperature Chart
# Author: Howard Webb
# Data: 7/25/2017
'''

from MultiChart import MultiChart

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
