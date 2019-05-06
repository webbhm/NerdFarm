'''
CO2 Chart
# Author: Howard Webb
# Data: 7/25/2017
'''

from MultiChart import MultiChart

SUBJECT="Air"
ATTRIBUTE="CO2"
FILE_NAME="/home/pi/MVP/web/co2_chart.svg"
LABEL="CO2"
UNITS="ppm"

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
