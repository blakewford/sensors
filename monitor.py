from machine import ADC,Pin,UART
import network
import socket
import time

ssid = ''
password = ''

def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        time.sleep(1)

    return wlan.ifconfig()[0]

ip = connect()

button = machine.Pin(26, machine.Pin.IN)
adc = ADC(Pin(27))
led = Pin("LED", Pin.OUT)

while True:
    if button.value():
        led.low()
    else:
        led.high()
    
    raw = adc.read_u16() & 0xFFF
    print((raw/4095)*1023)
    time.sleep(1)