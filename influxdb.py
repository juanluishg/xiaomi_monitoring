from dotenv import load_dotenv
import os
import time
from influxdb_client import InfluxDBClient, Point, WriteOptions

load_dotenv()  # take environment variables from .env.

INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
ORG = os.getenv("INFLUXDB_ORG")
HOST = os.getenv("INFLUXDB_HOST")
DATABASE = os.getenv("INFLUXDB_DATABASE")


def connect(host=HOST, token=INFLUXDB_TOKEN, org=ORG):
    client = InfluxDBClient(url=host, token=token, org=org)
    write_client = client.write_api(write_options=WriteOptions(batch_size=500,
                                                      flush_interval=10_000,
                                                      jitter_interval=2_000,
                                                      retry_interval=5_000,
                                                      max_retries=5,
                                                      max_retry_delay=30_000,
                                                      max_close_wait=300_000,
                                                      exponential_base=2))
    return write_client

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
    client.write(database, ORG, point)
    time.sleep(1) # separate points by 1 second

    print("Complete write air quality. Return to the InfluxDB UI.")
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
    client.write(database, ORG, point)
    time.sleep(1) # separate points by 1 second

    print("Complete write gpio. Return to the InfluxDB UI.")
    return True

def write_status(data:dict, client=connect()):
    database="sensor_data"

    point = (
        Point(data["model"])
        .tag("device_id", data["device_id"])
        .tag("source", data["source"])
        .tag("pin", data["pin"])
        .field("status", data["status"])
    )

    client.write(database, ORG, point)
    time.sleep(1) # separate points by 1 second

    print("Complete write status. Return to the InfluxDB UI.")
    return True

def close(client:InfluxDBClient):
    client.close()
