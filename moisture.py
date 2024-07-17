import machine

class moisture:
    def __init__(self, simulated):
        self.loop = 0
        self.accumulator = 0
        self.simulated = simulated

        if(not simulated):
            self.button = machine.Pin(26, machine.Pin.IN)
            self.adc = machine.ADC(machine.Pin(27))
            self.led = led = machine.Pin("LED", machine.Pin.OUT)
            
    def processAnalogInput(self):
        value = 1023.0
        if(not self.simulated):
            raw = self.adc.read_u16() & 0xFFF
            value = (raw/4095)*1023
            
        return value
    
    def processBinaryInput(self):
        if(not self.simulated):
            if self.button.value():
                return True
            else:
                return False
            
        return True