import json
import os
from flask import Flask, request

from utils import db_utils
from rest import process_payload

app = Flask(__name__)
app.url_map.strict_slashes = False

db_creds = json.loads(str(os.getenv('DB_CREDS')))
client = db_utils.get_connection(db_creds)

dbs = db_utils.get_dbs(client)


@app.route('/storage/', methods=['POST'])
def storage_request():
    data = request.json
    response = process_payload.process(data, dbs, db_creds)
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5007, debug=False)
