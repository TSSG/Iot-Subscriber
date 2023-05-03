import os
import json

import validate

temporal_fields = ["timestamp", "time"]
try:
    tags = os.environ['TAGS']
    if tags is not None:
        taggable_fields = json.loads(tags)
except json.decoder.JSONDecodeError:
    print("(Error): Tags must be supplied in the given format.")


def construct_data_item(pload):
    """Converts received payload to a format that can be inserted to InfluxDB, and populates fields and tags."""
    data_item = {}
    data_item["fields"] = {}
    data_item["tags"] = {}
    # Iterate through each key in the payload
    for key in pload.keys():
        if key == "measurement":
            data_item["measurement"] = pload["measurement"]
        # Validate the timestamp if one is found
        elif key in temporal_fields:
            resolved_time = validate.resolve_time(pload[key])
            data_item["time"] = resolved_time
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
                if key in taggable_fields:
                    data_item["tags"][key] = pload[key]
                else:
                    data_item["fields"][key] = pload[key]
            # Add payload dict to data_item to be inserted
            elif isinstance(pload[key], dict):
                data_item["fields"].update(pload[key])
            else:
                print("(Error): Could not process key " + key + " with value "+ str(pload[key]))
    return data_item

