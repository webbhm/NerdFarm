'''
Electrical Conductivity (EC) Chart
# Author: Howard Webb
# Data: 7/25/2017
'''

from MultiChart import MultiChart

SUBJECT="Nutrient"
ATTRIBUTE="EC"
FILE_NAME="/home/pi/MVP/web/ec_chart.svg"
LABEL="EC"
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
