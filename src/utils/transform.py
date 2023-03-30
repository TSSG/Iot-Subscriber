from utils import validate
temporal_fields=["timestamp", "time"]
to_be_ignored=["meta"]
taggable_fields = ["scenario", "mode", "id", "asset", "asset_id"]


def construct_data_item(pload, topic):
    """Converts received payload to a format that can be inserted to InfluxDB, and populates fields and tags."""
    data_item={}
    data_item["fields"] = {}
    tags = topic.copy()
    # Iterate through each key in the payload
    for key in pload.keys():
        # Validate the timestamp if one is found
        if key in temporal_fields:
            resolved_time = validate.resolve_time(pload[key])
            data_item["time"] = resolved_time
        # Add payload list to data_item to be inserted
        if isinstance(pload[key], list):
            if key not in to_be_ignored:
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
                        data_item["fields"][key+"_"+str(index_x)] = x
                        index_x+=1
        # Add payload value or string to data_item to be inserted
        elif isinstance(pload[key], (float, int, str)):
            if key not in to_be_ignored:
                # Determine if data is inserted as field or tag
                if key in taggable_fields:
                    tags[key] = pload[key]
                else:
                    data_item["fields"][key] = pload[key]
        # Add payload dict to data_item to be inserted
        elif isinstance(pload[key], dict):
            if key not in to_be_ignored:
                data_item["fields"].update(pload[key])
        else:
            print("(Transform): Could not process key " + key + " with value "+ str(pload[key]))
    data_item["tags"] = tags
    # Check if location is empty, if so, set to measurement
    if topic["location"] == '':
        data_item["measurement"] = topic["asset"]
    else:
        data_item["measurement"] = topic["location"]
    return data_item


def split_topic(topic):
    """Deconstructs MQTT topic to route data inserted to Influx"""
    tp_delim = {}
    tp = topic.split("/")
    ndx = 0
    for i in tp:
        if ndx == 0:
            tp_delim["location"] = i
        elif ndx == 1:
            tp_delim["asset"] = i
        elif ndx == 2:
            tp_delim["measurement"] = i
        else:
            tp_delim["taggable_"+str(ndx)] = i
        ndx+=1
    return tp_delim
