from dotenv import load_dotenv
import os
import time
from influxdb_client_3 import InfluxDBClient3, Point

load_dotenv()  # take environment variables from .env.

INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
ORG = os.getenv("INFLUXDB_ORG")
HOST = os.getenv("INFLUXDB_HOST")
DATABASE = os.getenv("INFLUXDB_DATABASE")


def connect(host=HOST, token=INFLUXDB_TOKEN, org=ORG):
    client = InfluxDBClient3(host=host, token=token, org=org)
    return client

def write(data:dict, client=connect()):
    database="sensor_data"

    point = (
        Point(data["model"])
        .tag("device_id", data["device_id"])
        .tag("ip", data["ip"])
        .tag("mac", data["mac"])
        .field(data["unit"], data["value"])
        .field("fault", data["fault"])
        .field("mode", data["mode"])
        .field("speed", data["speed"])
        .field("filter_used_time", data["filter_used_time"])
        .field("filter_life_level", data["filter_life_level"])
    )
    client.write(database=database, record=point)
    time.sleep(1) # separate points by 1 second

    print("Complete. Return to the InfluxDB UI.")
    return True

def write_gpio(data:dict, client=connect()):
    database="sensor_data"

    point = (
        Point(data["model"])
        .tag("device_id", data["device_id"])
        .tag("ip", data["ip"])
        .tag("mac", data["mac"])
        .field(data["unit"], data["value"])
    )
    client.write(database=database, record=point)
    time.sleep(1) # separate points by 1 second

    print("Complete. Return to the InfluxDB UI.")
    return True

def close(client:InfluxDBClient3):
    client.close()