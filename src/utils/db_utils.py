import time
import requests
from influxdb import InfluxDBClient

def store_reading(payload, client):
    """Stores payload in InfluxDB and reports result"""
    try:
        tags = payload["tags"]
        del payload["tags"]
        item = []
        item.append(payload)
        # Set to nanosecond precision
        resp = client.write_points(item, tags=tags, protocol=u'json', time_precision="n")
        return resp
    except AttributeError:
        raise AttributeError("The payload or topic cannot be processed or stored")

def get_connection(db_creds):
    """Returns an InfluxDB client"""
    try:
        return InfluxDBClient(db_creds["db_url"], db_creds["db_port"], db_creds["db_user"], db_creds["db_pass"], db_creds["db_name"])
    except Exception as e:
        print(e)

def get_dbs(client):
    """Returns a list of available databases for a given InfluxDB client"""
    dbs = []
    database_list = {}

    while not database_list:
        try:
            database_list = client.get_list_database()
        except requests.exceptions.ConnectionError:
            print("Could not connect to database. Waiting for connection...")
            time.sleep(60)

    for db in database_list:
        dbs.append(db["name"])

    return dbs
