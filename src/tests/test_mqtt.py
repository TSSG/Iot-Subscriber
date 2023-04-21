import unittest
import os
import unittest.mock as mock
import paho.mqtt.client as cl

import mqtt_interface

from exceptions import invalid_host

class TestMQTTConnection(unittest.TestCase):
    def test_successful_connection(self):
        mqtt_url = str(os.getenv('MQTTURL'))
        mqtt_user = str(os.getenv('MQTTUSER'))
        mqtt_pass = str(os.getenv('MQTTPASS'))
        mqtt_port = int(os.getenv('MQTTPORT'))  
        cli = mqtt_interface.connect(mqtt_url, mqtt_port, mqtt_user, mqtt_pass)
        self.assertTrue(cli.is_connected())

    def test_failed_connection_url_None(self):
        mqtt_user = str(os.getenv('MQTTUSER'))
        mqtt_pass = str(os.getenv('MQTTPASS'))
        mqtt_port = int(os.getenv('MQTTPORT')) 
        with self.assertRaises(invalid_host.InvalidHost):
            mqtt_interface.connect(None, mqtt_port, mqtt_user, mqtt_pass)

    def testMQTT_con(self):
        conn = mqtt_interface.connect_mqtt_client()
        self.assertTrue(conn.is_connected())

class TestDisconnect(unittest.TestCase):
    def test_successful_disconnect(self):
        mqtt_url = str(os.getenv('MQTTURL'))
        mqtt_user = str(os.getenv('MQTTUSER'))
        mqtt_pass = str(os.getenv('MQTTPASS'))
        mqtt_port = int(os.getenv('MQTTPORT'))  
        cli = mqtt_interface.connect(mqtt_url, mqtt_port, mqtt_user, mqtt_pass)
        cli.disconnect()
        self.assertFalse(cli.is_connected())

class TestOnMessage(unittest.TestCase):
    @mock.patch("process.process_payload")
    def test_on_message_success(self, mock_process):
        message = cl.MQTTMessage(topic='database1/measurement1'.encode('utf-8'))
        message.payload = b'{"time": "2022-07-06T09:10:00Z", "value": 5.292}'

        topic = 'database1/measurement1'
        payload = {'time': '2022-07-06T09:10:00Z', 'value': 5.292}
        db_creds = {"db_url":"my_db", "db_user":"admin", "db_pass":"admin", "db_port":8086, "db_name":"readings"}

        mqtt_interface.on_message(None, None, message)

        mock_process.assert_called_once_with(payload, topic, db_creds)