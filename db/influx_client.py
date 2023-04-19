import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "IFWM0UuKpXBf8imiUScqX1jMY57tzqi516LiuLxb4yVhfnc1Y6P-_6NTeaXySxQob-Gyeztu-RpnTYloW5lZEw=="
org = "Walton"
url = "http://localhost:8086"
bucket = "iot-sub"

def initialize_client(url, token, org):
    client = InfluxDBClient(url=url, token=token, org=org)
    return client

def write_data(client):
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for value in range(5):
        point = (
            Point("measurement1")
            .tag("tagname1", "tagvalue1")
            .field("field1", value)
        )
        write_api.write(bucket=bucket, org=org, record=point)
        time.sleep(1) # separate points by 1 second

def query_data(client):
    query_api = client.query_api()

    query = """from(bucket: "iot-sub")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "measurement1")"""
    tables = query_api.query(query, org="Walton")

    for table in tables:
        for record in table.records:
           print(record)

if __name__ == "__main__":
    client = initialize_client(url, token, org)
    write_data(client)
    query_data(client)








