# Author: Howard Webb
# Data: 7/25/2017
# Get temperature and send out as mqtt messge

from SI7021 import *
from oneWireTemp import *
from TSL2561 import getLux
from VL53L0X import *
import NDIR
import paho.mqtt.client as mqtt
from datetime import datetime
from time import sleep

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+mqtt.connack_string(rc))
    pass

def on_publish(client, userdata, mid):
    print "Published", userdata, " ", mid

def on_disconnect(client, userdata, rc):
    print "Disconnected: ", userdata, " Result: ", mqtt.connack_string(rc)

def pingMQTT(name, msg, test=False):
    host="iot.eclipse.org"
#    host="test.mosquitto.org"
    port=1883
    keepalive=60
    client = mqtt.Client()
#    print "Client: ", type(client)
    client.on_connect = on_connect
    client.on_publish=on_publish
    client.on_disconnect=on_disconnect
    q=client.connect(host=host, port=port, keepalive=keepalive)        
    print "Connection: host, port, keepalive ", host, port, keepalive
    topic='OpenAgBloom/' + name 
    result,mid=client.publish(topic, msg)
    client.disconnect()
    if test:
        print "Topic: ", topic, " Msg: ", msg
        print "Result: ", mqtt.connack_string(result), "Msg Id: ", mid

def msgTemp(test=False):
    si=SI7021()
    temp = si.get_tempC()
    msg='{:.2f}'.format(temp)
    pingMQTT('Air/Temp', msg, test)
    return msg
    

def msgHumidity(test=False):
    si=SI7021()
    h = si.get_humidity()
    msg='{:.2f}'.format(h)
    pingMQTT('Air/Humidity', msg, test)
    return msg

def msgCO2(test=False):
    sensor=NDIR.Sensor()
    sensor.begin()
    co2 = sensor.getCO2()
    msg='{:.2f}'.format(co2)
    pingMQTT('Air/CO2', msg, test)
    return msg

def msgDepth(test=False):
    ds=VL53L0X()
    dist=ds.getDistance()
    msg='{:3.1f}'.format(dist)
    pingMQTT('Nutrient/Distance', msg, test)
    return msg

def msgLUX(test=False):
    lux=getLux()
    msg='{:3.1f}'.format(lux)
    pingMQTT('Light/Lux', msg, test)
    return msg

def msgTopTemp(test=False):
    temp=getTempC(topTemp)
    msg='{:3.1f}'.format(temp)
    pingMQTT('Top/Temp', msg, test)
    return msg

def msgAmbientTemp(test=False):
    temp=getTempC(ambientTemp)
    msg='{:3.1f}'.format(temp)
    pingMQTT('Ambient/Temp', msg, test)
    return msg

def msgBoxTemp(test=False):
    temp=getTempC(boxTemp)
    msg='{:3.1f}'.format(temp)
    pingMQTT('Box/Temp', msg, test)
    return msg

def msgReservoirTemp(test=False):
    temp=getTempC(reservoirTemp)
    msg='{:3.1f}'.format(temp)
    pingMQTT('Reservoir/Temp', msg, test)
    return msg


def test():
    print "Send Temp"
    msg=msgTemp(True)
    print "Temp: ", msg

    sleep(5)
    
    print "Send Humidity"
    msg=msgHumidity(True)
    print "Humidity: ", msg

    sleep(5)

    print "Send CO2"
    msg=msgCO2(True)
    print "CO2: ", msg

    sleep(5)    

#    print "Send Distanace"
#    msg=msgDepth(True)
#    print "Distanace: ", msg

#    sleep(5)    

    print "Send LUX"
    msg=msgLUX(True)
    print "LUX: ", msg

    sleep(5)    

    print "Send Ambient Temp"
    msg=msgAmbientTemp(True)
    print "Ambient Temp: ", msg
    
    sleep(5)    

    print "Top Temp"
    msg=msgTopTemp(True)
    print "Top Temp: ", msg

    sleep(5)    

    print "Box Temp"
    msg=msgBoxTemp(True)
    print "Box Temp: ", msg

    sleep(5)    

    print "Reservoir Temp"
    msg=msgReservoirTemp(True)
    print "ReservoirTemp: ", msg

def test2():
    print "Test Connection"
    msg="TEST"
    pingMQTT('Test', msg, True)
    
if __name__=="__main__":
    test()
