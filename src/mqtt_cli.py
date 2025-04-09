import paho.mqtt.client as paho
import time

from exceptions import invalid_host


class MqttClient(object):


    def __init__(self, **kwargs):

        client_nm = "subscriber-base"
        if "name" in kwargs:
            client_nm = kwargs["name"]
        self.mq_client = paho.Client(paho.CallbackAPIVersion.VERSION1, client_nm, True)
        self.connected = False


    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print("Connected to MQTT Message Broker")
            topic = "#"
            self.mq_client.subscribe(topic)
            msg = "Subscribed to: " + topic
            print(msg)
        else:
            print("Failed to connect to MQTT Message Broker")


    def on_disconnect(self, client, userdata, rc):
        if rc == 0:
            self.connected = False
            print("Disconnected from MQTT Message Broker")
        else:
            print("Unexpected disconnect... Response code: " + str(rc))


    def disconnect(self):
        try:
            self.mq_client.disconnect()
            self.mq_client.loop_stop()
        except Exception as error:
            print("Disconnect error")
            print(str(error))
        return


    def subscribe(self, topic):
        return self.mq_client.subscribe(topic, 2)


    def unsubscribe(self, topic):
        return self.mq_client.unsubscribe(topic)


    def get_client(self):
        return self.mq_client


    def is_connected(self):
        return self.connected


    def publish(self, topic, payload):
        # Publish data to mqtt broker
        self.mq_client.publish(topic, payload)


    def connect(self, url, on_message, **kwargs):
        if url == "" or url is None:
            raise invalid_host.InvalidHost("%s is not a valid url for connection" %url)
        try:
            self.mq_client.on_connect = self.on_connect
            self.mq_client.on_disconnect = self.on_disconnect
            self.mq_client.on_message = on_message
            mqtt_port = 1883
            if "port" in kwargs:
                mqtt_port = kwargs["port"]
            if mqtt_port == 8883:
                self.mq_client.username_pw_set(kwargs["user"], kwargs["passwd"])
                self.mq_client.connect(
                    url,
                    port = mqtt_port,
                    keepalive = 5)
            else:
                self.mq_client.connect(url, port = mqtt_port, keepalive=5)
            self.mq_client.loop_start()
            while not self.connected:
                time.sleep(0.1)
        except Exception as error:
            print("Connect Error:", error)
            raise 