from time import sleep
from datetime import datetime
from gpiozero import MCP3008
import Adafruit_DHT
import time

def read():
    min = 350.0
    max = 1023.0
    sensor = Adafruit_DHT.DHT11
    sensor_pin = 4
    
    while True:
        pot = MCP3008(channel=0, device=0)
        now = datetime.now()
        print(pot.raw_value)
        print("Soil moisture {}".format(((pot.raw_value - max)/(min-max))*100))
        print("Timestamp {}".format(now.strftime("%H:%M:%S")))
        print("----------------------------------")
        pot.close()
        humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)  # Use read_retry to retry in case of failure
        if humidity is not None and temperature is not None:
            # Uncomment the line below to convert to Fahrenheit
            temperatureF = temperature * 9/5.0 + 32
            print("Temp={0:0.1f}ºC, Temp={1:0.1f}ºF, Humidity={2:0.1f}%".format(temperature, temperatureF, humidity))
        else:
            print("Sensor failure. Check wiring.")
        sleep(3)

if __name__ == "__main__":
    read()

# Complete Project Details: https://RandomNerdTutorials.com/raspberry-pi-dht11-dht22-python/



# comment and uncomment the lines below depending on your sensor

# sensor = Adafruit_DHT.DHT11

# DHT pin connects to GPIO 4

    
