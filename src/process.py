import db_utils


def process_payload(data, topic, db_creds):
    """Checks if the expected database name is valid and forms a response to the REST request"""

    client = db_utils.get_connection(db_creds)

    try:
        if not isinstance(data, dict):
            print("(Error): Payload must be in json format:\n", str(data))
            return 1
        try:
            split_topic = topic.split("/")
            bucket = split_topic[0]
            measurement = split_topic[1]
            tags = split_topic[:2]
        except KeyError as error:
            print("(Error): Topic is not in the required format:\n", str(topic))
            return 1

        data["measurement"] = measurement
        valid_pload = validate_data(data, tags)

        db_utils.store_reading(valid_pload, client, bucket)
        return 0
    except Exception as error:
        print("(Error): Could not process data:\n", print(str(error)))
        return 1

def validate_data(pload, tags):
    """Checks if incoming payload can be stored or transformed for storage"""
    required_keys = ["fields", "time", "measurement"]
    # Payload is valid if each required key appears in it
    if all(k in pload.keys() for k in required_keys):
        valid_pload = pload
    elif "time" in pload.keys():
        valid_pload = construct_data_item(pload, tags)
    else:
        raise KeyError("KeyError: '", str(pload), "' cannot be inserted into database.")

    return valid_pload

def construct_data_item(pload, tags):
    """Converts received payload to a format that can be inserted to InfluxDB, and populates fields and tags."""
    data_item = {}
    data_item["fields"] = {}
    data_item["tags"] = {}

    # Iterate through each key in the payload
    for key in pload.keys():
        if key == "measurement":
            data_item["measurement"] = pload["measurement"]
        else:
            # Add payload list to data_item to be inserted
            if isinstance(pload[key], list):
                index_x = 1
                # Flatten list to individual elements
                for x in pload[key]:
                    if isinstance(x, list):
                        index_y = 1
                        # Flatten nested list
                        for y in x:
                            data_item["fields"][key+"_"+str(index_x)+"_"+str(index_y)] = y
                            index_y+=1
                        index_x+=1
                    else:
                        data_item["fields"][key+"_" + str(index_x)] = x
                        index_x+=1
            # Add payload value or string to data_item to be inserted
            elif isinstance(pload[key], (float, int, str)):
                # Determine if data is inserted as field or tag
                if key == "time":
                    data_item["time"] = pload["time"]
                elif key in tags:
                    data_item["tags"][key] = pload[key]
                else:
                    data_item["fields"][key] = pload[key]
            # Add payload dict to data_item to be inserted
            elif isinstance(pload[key], dict):
                data_item["fields"].update(pload[key])
            else:
                print("(Error): Could not process key " + key + " with value "+ str(pload[key]))
    return data_item
