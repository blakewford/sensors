from machine import ADC,Pin,UART
import network
import socket
import time

ssid = ''
password = ''

mqtt_port = 1883

# Control packet type
RESERVED=0,
CONNECT=1,
CONNACK=2,
PUBLISH=3,
PUBACK=4,
PUBREC=5,
PUBREL=6,
PUBCOMP=7,
SUBSCRIBE=8,
SUBACK=9,
UNSUBSCRIBE=10,
UNSUBACK=11,
PINGREQ=12,
PINGRESP=13,
DISCONNECT=14,
#RESERVED=15

class mqtt:
    def connect(address, username, password):
        return
    def publish(topic, message):
        return
    def disconnect():
        return

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        time.sleep(1)

    return wlan.ifconfig()[0]

ip = connect()
mq = mqtt(address=ip,username='',password='')

button = machine.Pin(26, machine.Pin.IN)
adc = ADC(Pin(27))
led = Pin("LED", Pin.OUT)

while True:
    if button.value():
        led.low()
    else:
        led.high()
    
    raw = adc.read_u16() & 0xFFF
    value = (raw/4095)*1023
    print(value)
    time.sleep(1)