import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "QrByyn1unXvqZFjsEXG3ItLijVxP8vsr8QL0qVAMLh6ZArW5P2rbAPF7s10xb9i_8B8ap5iuLCPW-6loY6Ixdw=="
org = "Walton"
url = "http://localhost:8086"
bucket = "Walton"

def initialize_client(url, token, org):
    client = InfluxDBClient(url=url, token=token, org=org)
    return client


def query_data(client):
    query_api = client.query_api()

    query = """from(bucket: "Walton")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "measurement1")"""
    tables = query_api.query(query, org="Walton")

    for table in tables:
        for record in table.records:
           print(record)

if __name__ == "__main__":
    client = initialize_client(url, token, org)

    query_data(client)








