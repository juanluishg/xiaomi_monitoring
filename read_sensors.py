from time import sleep
from datetime import datetime
from gpiozero import MCP3008
import Adafruit_DHT
import time
import influxdb
from influxdb_client import InfluxDBClient
import os
from getmac import get_mac_address as gma
import socket
import pump_controller as pump

LAST_PUMP_STATUS=0

def get_ip_address():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

def get_soil_moisture(channel=0, device=0, min_moisture=350.0, max_moisture=1023.0):
    global LAST_PUMP_STATUS
    pot = MCP3008(channel=channel, device=device)
    now = datetime.now()
    print(pot.raw_value)
    moisture_value=((pot.raw_value - max_moisture)/(min_moisture-max_moisture))*100
    print("Soil moisture {}".format(moisture_value))
    print("Timestamp {}".format(now.strftime("%H:%M:%S")))
    if(moisture_value < 20 and LAST_PUMP_STATUS == 0):
        pump.on_off(True)
        LAST_PUMP_STATUS=1
    elif (moisture_value > 20):
        pump.on_off(False)
        LAST_PUMP_STATUS=0
    pot.close()
    return moisture_value

def get_hum_temp(sensor_pin=4):
    sensor = Adafruit_DHT.DHT11
    humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)  # Use read_retry to retry in case of failure
    now = datetime.now()
    if humidity is not None and temperature is not None:
        # Uncomment the line below to convert to Fahrenheit
        temperatureF = temperature * 9/5.0 + 32
        print("Temp={0:0.1f}ºC, Temp={1:0.1f}ºF, Humidity={2:0.1f}%".format(temperature, temperatureF, humidity))
        print("Timestamp {}".format(now.strftime("%H:%M:%S")))
        return temperature, temperatureF, humidity
    else:
        print("Sensor failure. Check wiring.")
        print("Timestamp {}".format(now.strftime("%H:%M:%S")))
        return None, None, None
    
def get_every_n_seconds(db_client, seconds=10, channel=0, device=0, min_moisture=350.0, max_moisture=1023.0, sensor_pin=4):
    while True:
        moisture = get_soil_moisture(channel, device, min_moisture, max_moisture)
        data = create_json('soil_'+str(channel)+'_'+str(device), moisture, gma(), 'M5' , '%' ,get_ip_address())
        write_to_influx(data, db_client)
        temperature, _ , humidity = get_hum_temp(sensor_pin)
        if temperature is not None and humidity is not None:
            data = create_json('hum_'+str(sensor_pin), humidity, gma(), 'DHT11', '%', get_ip_address())
            write_to_influx(data, db_client)
            data = create_json('temp_'+str(sensor_pin), temperature, gma(), 'DHT11', 'celsius', get_ip_address())
            write_to_influx(data, db_client)
        
        sleep(seconds)

def write_to_influx(data:dict, client: InfluxDBClient=influxdb.connect()):
    print(f"Writing to influx db:\n{data}")
    return influxdb.write_gpio(data,client)

def create_json(id:str, 
                value:str, 
                mac: str, 
                model: str, 
                unit: str, 
                ip:str):
    res = {
        "device_id": id,
        "mac": mac,
        "model": model,
        "value": int(value),
        "unit": unit,
        "ip": ip
    }
    return res

def main(refresh_seconds=30):
    db_client = None
    try:
        db_client = influxdb.connect()
        get_every_n_seconds(db_client, refresh_seconds)
    except Exception as e:
        db_client.close()
        print("Read sensors: {}".format(e))
        print("Closing all. Chao ;P")
        exit(0)

    
