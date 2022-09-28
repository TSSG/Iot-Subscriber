import json
from influxdb import InfluxDBClient
from flask import Flask, request

from rest import process_payload

app = Flask(__name__)
app.url_map.strict_slashes = False

# client = InfluxDBClient(host='', port='', username='', password='')
# dbs = client.get_list_database()
dbs = ['AGC']


@app.route('/storage/', methods=['POST'])
def storage_request():
    try:
        data = None
        data = request.json

        if data['measurement'] in dbs:
            summary = process_payload.store_data(data)
        else:
            return json.dumps({"success": False, "Description": '"Bad Request: ' + data["measurement"] + ' database has not been created."'}), 400, {'ContentType': 'application/json'}

        return json.dumps(summary), 200, {'ContentType': 'application/json'}
    except Exception as error:
        return json.dumps({"success": False, "Description": '"Bad Request: ' + str(error) + '"'}), 400, {'ContentType': 'application/json'}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5007, debug=False)
