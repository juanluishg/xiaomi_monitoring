# Xiaomi Airpurifier 4 Compact to InfluxDB

## Installation

```pip install -r requirements.txt```

## Configuration

Create a .env file and write inside the following variables:

* INFLUXDB_TOKEN
* INFLUXDB_ORG
* INFLUXDB_HOST
* INFLUXDB_DATABASE
* XIAOMI_USER
* XIAOMI_PASSWORD

## Running

```python get_air_quality.py```

## References

### Repos

* https://github.com/OneB1t/AirQualityXiaomiMonitor
* https://github.com/rytilahti/python-miio/tree/master
* https://github.com/Squachen/micloud

### Issues

* https://github.com/rytilahti/python-miio/issues/1550
* https://github.com/rytilahti/python-miio/pull/1581

### Docs

* https://home.miot-spec.com/spec/zhimi.airp.cpa4
* https://python-miio.readthedocs.io/en/latest/api/miio.device.html