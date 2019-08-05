'''
Create Environment and Trials
# Build dictionary structure variables for the environment
# A python file is generated that is 'read' by the logging program.
# Author: Howard Webb
# Data: 2/21/2018
'''

import uuid
import json
from datetime import datetime

def makeTrial():
    from env import env
    env['trials'] = Trials()
    saveDict('env', '/home/pi/MVP/python/env.py', env)
    
def Trials():
    trials = []
    timestamp = datetime.utcnow().isoformat()[:19]
    id = str(uuid.uuid4())
    trials = [{'id':id, 'start_date':timestamp}]
    return trials

def prettyPrint(txt):
    '''Dump json in nice format'''
    #print type(txt)
    print(json.dumps(txt, indent=4, sort_keys=True))

def saveDict(name, file_name, dict):
    #print(values)
    f = open(file_name, 'w+')
    tmp=name+'='+str(dict)
    f.write(tmp)
    f.close()
    
def test():
    makeTrial()
    from env import env
    prettyPrint(env)

if __name__=="__main__":
    test()
    
    
    


    
