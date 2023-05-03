from random import randint
from mqtt_cli import MqttClient as mqc
import os
import time
import ssl
import json
import traceback

import process
from exceptions import invalid_host

rand = randint(1000000000, 9999999999)

client = mqc(name = "iot-subscriber-" + str(rand))


def on_message(client, userdata, message):
    topic = message.topic
    try:
        message_txt = message.payload.decode("utf-8").replace("\x00", "")
        pload = json.loads(message_txt)
        if 'data' in pload.keys():
            return process.process_payload(pload['data'], topic)
        else:
            return process.process_payload(pload, topic)
    except Exception as error:
        print("(Main) On message error:\n" + str(error))
        traceback.print_exc()


def connect_mqtt_client():
    mqtt_url = str(os.getenv('MQTTURL'))
    mqtt_user = str(os.getenv('MQTTUSER'))
    mqtt_pass = str(os.getenv('MQTTPASS'))
    try:
        mqtt_port = int(os.getenv('MQTTPORT'))
    except TypeError:
        mqtt_port = 1883
    return connect(mqtt_url, mqtt_port, mqtt_user, mqtt_pass)


def connect(mqtt_url, mqtt_port, mqtt_user, mqtt_pass):
    try:
        if mqtt_port == 8883:
            client.connect(
                mqtt_url,
                on_message,
                port = mqtt_port,
                ssl = ssl.PROTOCOL_TLSv1_2,
                user = mqtt_user,
                passwd = mqtt_pass
         )
        else:
            try:
                client.connect(mqtt_url, on_message)
                return client
            except invalid_host.InvalidHost:
                raise invalid_host.InvalidHost("%s is not a valid url for connection" %mqtt_url)
            except Exception as e:
                print(e)
        while True:
            time.sleep(1)
    except invalid_host.InvalidHost:
        raise invalid_host.InvalidHost("%s is not a valid url for connection" %mqtt_url)
    except Exception as e:
        print(e)