import time
from sys import platform

from moisture import moisture
from mqtt import mqtt
from temperature import temperature

ssid = ''
network_password = ''

mqtt_username = ''
mqtt_password = ''

simulated = platform == 'linux'
if(not simulated):
    import network

def networkConnect():
    if(not simulated):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, network_password)
        while wlan.isconnected() == False:
            time.sleep(1)

        return wlan.ifconfig()[0]
    else:
        return '192.168.1.1'

ip = networkConnect()
mq = mqtt(address=ip,username=mqtt_username,password=mqtt_password, simulated=simulated)
moist = moisture(simulated)
temp = temperature(-2, simulated)

mq.connect()
while True:
    value = moist.processAnalogInput()
    dry = moist.processBinaryInput()
    mq.publish("MOISTURE", str(value))
    mq.publish("DRY", str(dry))
    mq.publish("TEMPERATURE", str(temp.readTemperatureF()))
    time.sleep(1)