import validate
import db_utils


def process_payload(data, topic, db_creds):
    """Checks if the expected database name is valid and forms a response to the REST request"""
    client = db_utils.get_connection(db_creds)

    dbs = db_utils.get_dbs(client)

    try:
        if not isinstance(data, dict):
            print("(Error): Payload must be in json format:\n", str(data))
            return 1
        try:
            db = (topic.split("/"))[0]
            measurement = (topic.split("/")[1])
        except KeyError as error:
            print("(Error): Topic is not in the required format:\n", str(topic))
            return 1

        if db in dbs:
            storage_creds = db_creds
            storage_creds['db_name'] = db
            client = db_utils.get_connection(storage_creds)
            data["measurement"] = measurement
            valid_pload = validate.validate_data(data)

            result = db_utils.store_reading(valid_pload, client)
            if result:
                return 0
            else:
                print("(Error): Payload could not be inserted:\n", str(valid_pload))
                return 1
        else:
            print("(Error): Database '", db, "' has not been created.")
            return 1
    except Exception as error:
        print("(Error): Could not process data:\n", print(str(error)))
        return 1

