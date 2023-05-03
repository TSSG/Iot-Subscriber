import os
import validate
import db_utils


def process_payload(data, topic):
    """Checks if the expected database name is valid and forms a response to the REST request"""
    db_creds = {}
    db_creds["url"] = str(os.getenv("DB_URL"))
    db_creds["org"] = str(os.getenv("DB_ORG"))
    db_creds["token"] = str(os.getenv("DB_TOKEN"))

    client = db_utils.get_connection(db_creds)

    try:
        if not isinstance(data, dict):
            print("(Error): Payload must be in json format:\n", str(data))
            return 1
        try:
            bucket = (topic.split("/"))[0]
            measurement = (topic.split("/")[1])
        except KeyError as error:
            print("(Error): Topic is not in the required format:\n", str(topic))
            return 1

        data["measurement"] = measurement
        valid_pload = validate.validate_data(data)

        result = db_utils.store_reading(valid_pload, client, bucket)
        if result:
            return 0
        else:
            print("(Error): Payload could not be inserted:\n", str(valid_pload))
            return 1
    except Exception as error:
        print("(Error): Could not process data:\n", print(str(error)))
        return 1

