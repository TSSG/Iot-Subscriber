import os
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS


def store_reading(payload, client, bucket):
    """Stores payload in InfluxDB"""
    precision = str(os.getenv("PRECISION"))

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=bucket, record=payload, write_precision=precision)

def get_connection(db_creds):
    """Returns an InfluxDB client"""
    try:
        return InfluxDBClient(url=db_creds["url"], token=db_creds["token"], org=db_creds["org"])
    except Exception as e:
        print(e)