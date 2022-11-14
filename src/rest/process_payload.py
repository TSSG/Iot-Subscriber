import json

from utils import validate, transform, db_utils


def process(data, dbs, db_creds):
    """Checks if the expected database name is valid and forms a response to the REST request"""
    try:
        if not isinstance(data, dict):
            return json.dumps({"success": False, "Description": "Request must be in JSON format."}), 400, {'ContentType': 'application/json'}
        try:
            topic = data['topic']
            db = (topic.split("/"))[0]
        except KeyError as error:
            return json.dumps({"success": False, "Description": "Request is not in the required format."}), 400, {'ContentType': 'application/json'}

        if db in dbs:
            storage_creds = db_creds
            storage_creds['db_name'] = db
            storage_client = db_utils.get_connection(storage_creds)
            summary, status_code = store_data(data, storage_client)
        else:
            return json.dumps({"success": False, "Description": '"Bad Request: "' + db + '" database has not been created."'}), 400, {'ContentType': 'application/json'}

        return json.dumps(summary), status_code, {'ContentType': 'application/json'}
    except Exception as error:
        return json.dumps({"success": False, "Description": '"Bad Request: ' + str(error) + '"'}), 400, {'ContentType': 'application/json'}


def store_data(data, client):
    """Routes the data for validation, transformation and storage and checks if storage was successful"""
    payload = data['payload']
    print("payload ", payload)
    # Strip database name from topic
    measurement = data['topic'].partition("/")[2]
    topic = transform.split_topic(measurement)
    print("topic ", topic)

    valid_pload = validate.validate_data(payload, topic)
    print("valid pload", str(valid_pload))

    result = db_utils.store_reading(valid_pload, client)

    if result:
        summary = {"success": True, "Description": "Payload stored successfully."} 
        status_code = 200
    else:
        summary = {"success": False, "Description": "Could not store payload: \npayload: '" + str(valid_pload) + "' \ntopic: '" + str(topic) + "'"}
        status_code = 400

    return summary, status_code
