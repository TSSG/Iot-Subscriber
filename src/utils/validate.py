import re
import json
import dateutil.parser
from datetime import datetime

from utils import transform

required_keys = ["fields", "time", "measurement"]
fields = ["scenario", "mode", "id", "asset", "asset_id"]


def validate_data(pload, topic):
    """Checks if incomign payload can be stored or transformed for storage"""
    # Payload is valid if each required key appears in it
    if all(k in pload.keys() for k in required_keys):
        valid_pload = pload
    # Check if data can be transformed
    elif any(k in pload.keys() for k in fields):
        valid_pload = transform.construct_data_item(pload, topic)
    else:
        raise KeyError("KeyError: '", str(pload), "' cannot be inserted into database.")

    resolved_time = resolve_time(pload["time"])
    valid_pload["time"] = resolved_time

    return valid_pload


def resolve_time(time):
    if str(time).isdigit():
        dateobj = dateutil.parser.parse(datetime.utcfromtimestamp(int(time)/1000000000).strftime('%Y-%m-%d %H:%M:%S.%f'), dayfirst=True)
        return str(dateobj)
    else:
        if validate_ddmmyy(time):
            dateobj = dateutil.parser.parse(time, dayfirst=True)
            return str(dateobj)
        elif validate_iso8601(time):
            dateobj = dateutil.parser.parse(time, dayfirst=False)
            return str(dateobj)
        else:
            print("The value "+str(time)+ " could not be converted to a UTC time adding now as the timestamp")
            return datetime.utcnow()

def validate_iso8601(str_val):
    regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])(T| )(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    match_iso8601 = re.compile(regex).match
    try:
        if match_iso8601(str_val) is not None:
            return True
        else:
            return False
    except Exception as e:
        return False

def validate_ddmmyy(str_val):
    regex = r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$'
    match_ddmmyy = re.compile(regex).match
    try:
        if match_ddmmyy(str_val) is not None:
            return True
        else:
            return False
    except Exception as e:
        return False
