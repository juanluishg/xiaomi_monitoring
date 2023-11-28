from micloud import MiCloud
from miio import DeviceFactory, DeviceInfo, Device
from time import sleep
import influxdb
from influxdb_client import InfluxDBClient
from dotenv import load_dotenv
import os

USERNAME=os.getenv("XIAOMI_USER")
PASSWORD=os.getenv("XIAOMI_PASSWORD")

FAULT = {
    0:"No Faults",
    2:"Motor Stuck",
    3:"Sensor Lost"
}
MODE = {
    0:"Auto",
    1:"Sleep",
    2:"Favorite"
}

def read_password(path="password"):
    f = open("password", "r")
    return f.read()

def connect(username=USERNAME, password=PASSWORD, path=None):
    if(password == None):
        password = read_password(path) if path is not None else read_password()
    mc = MiCloud(username, password)
    mc.login()
    token = mc.get_token() # to get your cloud service token.
    device_list = mc.get_devices() # get list of devices
    dev = DeviceFactory.create(device_list[0]["localip"], device_list[0]["token"])
    return dev

def get_air_quality(device: Device):
    prop = device.raw_command("get_properties", [{"siid":3,"piid":4}])
    return prop[0]['value']

def get_fault(device: Device):
    prop = device.raw_command("get_properties", [{"siid":2,"piid":2}])
    return prop[0]['value']

def get_mode(device: Device):
    prop = device.raw_command("get_properties", [{"siid":2,"piid":4}])
    return prop[0]['value']

def get_speed(device: Device):
    prop = device.raw_command("get_properties", [{"siid":9,"piid":1}])
    return prop[0]['value']

def get_filter_used_time(device: Device):
    prop = device.raw_command("get_properties", [{"siid":4,"piid":3}])
    return prop[0]['value']

def get_filter_life_level(device: Device):
    prop = device.raw_command("get_properties", [{"siid":4,"piid":1}])
    return prop[0]['value']

def info(device: Device):
    print("Print device information: ") 
    print(device.info())
    
def get_every_n_seconds(device: Device, client: InfluxDBClient, seconds=10):
    while True:
        value = get_air_quality(device)
        print(f"Quality: {value} μg/m^3")
        info: DeviceInfo = device.info()
        data = create_json(device.device_id, value, info.mac_address, device.model, "μg/m^3", 
                           info.ip_address, get_fault(device), get_mode(device), get_speed(device),
                           get_filter_used_time(device), get_filter_life_level(device))
        write_to_influx(data, client)
        sleep(seconds)

def write_to_influx(data:dict, client: InfluxDBClient=influxdb.connect()):
    print(f"Writing to influx db:\n{data}")
    return influxdb.write(data,client)

def create_json(id:str, 
                value:str, 
                mac: str, 
                model: str, 
                unit: str, 
                ip:str, 
                fault:str, 
                mode:str, 
                speed:str, 
                filter_used_time: str, 
                filter_life_level:str):
    res = {
        "device_id": id,
        "mac": mac,
        "model": model,
        "value": int(value),
        "unit": unit,
        "ip": ip,
        "fault": FAULT[int(fault)],
        "mode": MODE[int(mode)],
        "speed": int(speed),
        "filter_used_time": int(filter_used_time),
        "filter_life_level": int(filter_life_level)
    }
    return res

def main(args=[]):
    db_client = None
    try:
        dev = connect()
        db_client = influxdb.connect()
        info(dev)
        get_every_n_seconds(dev, db_client, 30)
    except KeyboardInterrupt:
        db_client.close()
        print("Closing all. Chao ;P")
        exit(0)

if __name__ == '__main__':
    main()
    
    