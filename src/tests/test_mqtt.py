import unittest
import unittest.mock as mock
import paho.mqtt.client as cl

import mqtt_interface


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