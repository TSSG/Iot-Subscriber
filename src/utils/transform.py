from utils import validate
temporal_fields=["timestamp", "time"]
to_be_ignored=["meta"]
taggable_fields = ["scenario", "mode", "id", "asset", "asset_id"]


def construct_data_item(pload, topic):
    data_item={}
    data_item["fields"] = {}
    tags = topic.copy()
    for k in pload.keys():
        if k in temporal_fields:
            resolved_time = validate.resolve_time(pload[k])
            data_item["time"] = resolved_time
        if isinstance(pload[k], list):
            if k not in to_be_ignored:
                ndx = 1
                for i in pload[k]:
                    if isinstance(i, list):
                        dx = 1
                        for p in i:
                            data_item["fields"][k+"_"+str(ndx)+"_"+str(dx)] = p
                            dx+=1
                        ndx+=1
                    else:
                        data_item["fields"][k+"_"+str(ndx)] = i
                        ndx+=1
        elif isinstance(pload[k], (float, int)):
            if k not in to_be_ignored:
                if k in taggable_fields:
                    tags[k] = pload[k]
                else:
                    data_item["fields"][k] = pload[k]
        elif isinstance(pload[k], dict):
            if k not in to_be_ignored:
                data_item["fields"].update(pload[k])
        elif isinstance(pload[k], str):
            if k not in to_be_ignored:
                if k in taggable_fields:
                    tags[k] = pload[k]
                else:
                    data_item["fields"][k] = pload[k]
        else:
            print(k+"not sure what k is but it has a value of \n "+ str(pload[k]))
    data_item["tags"] = tags
    # Check if location is empty, if so, set to measurement
    if topic["location"] == '':
        data_item["measurement"] = topic["asset"]
    else:
        data_item["measurement"] = topic["location"]
    return data_item


def split_topic(topic):
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
