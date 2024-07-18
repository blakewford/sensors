import machine

class temperature:
    def __init__(self, calibration, simulated):
        self.simulated = simulated
        self.calibration = calibration
        if(not simulated):
            temperature_pin = 4
            self.sensor = machine.ADC(temperature_pin)
  
    def readTemperatureC(self):
        value = 14000
        if(not self.simulated):
            value = self.sensor.read_u16()
        volt = (3.3/65535) * value
        base = 27 - (volt - 0.706)/0.001721

        return round(base, 1) + self.calibration

    def readTemperatureF(self):
        return self.readTemperatureC()*9/5 + 32