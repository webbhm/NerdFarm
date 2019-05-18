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

def main(level=MultiChart.INFO):
    ''' Function to test the chart building with test flag set to True
           Args:
               level: logging level, defaults to debug
           Returns:
               None:
           Raises:
               None
    '''
    chart = MultiChart(SUBJECT, ATTRIBUTE, LABEL, UNITS, FILE_NAME)
    chart.setLevel(level)
    chart.buildMultiChart()
    
def validate():
    ''' Validation function, info level logging
           Args:
               level: logging leve
           Returns:
               None:
           Raises:
               None
    '''
    
    main(MultiChart.INFO)
    
def test():
    ''' Test function, debug level logging
           Args:
               level: logging leve
           Returns:
               None:
           Raises:
               None
    '''
    
    main(MultiChart.DEBUG)        

if __name__=="__main__":
    validate()
