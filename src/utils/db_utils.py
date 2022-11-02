import ast
import os
import time
import traceback
import requests
from utils import transform
from influxdb import InfluxDBClient

debug_enabled = ast.literal_eval(str(os.getenv('DEBUG')))

def store_reading(payload, topic, client):
    try:
        data_item = transform.construct_data_item(payload, topic)
        tags = data_item["tags"]
        del data_item["tags"]
        if debug_enabled:
            print(tags)
            print(data_item)
        item = []
        item.append(data_item)
        # Set to nanosecond precision
        resp = client.write_points(item, tags=tags, protocol=u'json', time_precision="n")
        return resp
    except AttributeError:
        raise AttributeError("The payload or topic cannot be processed or stored")

def get_connection(db_creds):
    try:
        return InfluxDBClient(db_creds["db_url"], db_creds["db_port"], db_creds["db_user"], db_creds["db_pass"], db_creds["db_name"])
    except Exception as e:
        print(e)

def get_dbs(client):
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
