import io_serial as pump
import time
import influxdb
from influxdb_client import InfluxDBClient
from datetime import datetime

def turn_on_pump(client: InfluxDBClient=influxdb.connect()):
    arduino = pump.get_arduino("/dev/ttyACM0")
    time.sleep(2)
    print(pump.write("on",arduino))
    arduino.close()
    write_status_influx({"model":"dollatek","device_id":"pump_8", "source":"/dev/ttyACM0", "pin":8, "status": 1}, client)

def turn_off_pump(client: InfluxDBClient=influxdb.connect()):
    arduino = pump.get_arduino("/dev/ttyACM0")
    time.sleep(2)
    print(pump.write("off",arduino))
    arduino.close()
    write_status_influx({"model":"dollatek","device_id":"pump_8", "source":"/dev/ttyACM0", "pin":8, "status": 0}, client)

def write_status_influx(status: dict, client: InfluxDBClient=influxdb.connect()):
    print(f"Writing to influx db:\n{status}")
    return influxdb.write_status(status,client)

def on_off(on=False):
    try:
        db_client = influxdb.connect()
        if(on):
            turn_on_pump(db_client)
        else:
            turn_off_pump(db_client)
        db_client.close()
    except Exception as e:
        print("Pump controller: {}".format(e))
        print("Closing all. Chao ;P")
        exit(0)