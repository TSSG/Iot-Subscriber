import unittest
import json
from unittest.mock import patch, MagicMock

from utils import db_utils


class TestStore(unittest.TestCase):
    def test_store_reading(self):
        topic = json.loads('{"location": "location_9000", "asset": "9000", "measurement": "operationPower"}')
        payload = json.loads('{"time": "2022-01-01 00:00:00.000", "value": 123.456}')

        client = MagicMock()

        with patch.object(client, 'write_points') as mock_write_points:
            db_utils.store_reading(payload, topic, client)

        mock_write_points.assert_called()

    def test_store_reading_invalid_date(self):
        topic = json.loads('{"location": "location_9000", "asset": "9000", "measurement": "operationPower"}')
        payload = json.loads('{"time": "2022-1 00:00:00.000", "value": 123.456}')

        client = MagicMock()

        with patch.object(client, 'write_points') as mock_write_points:
            db_utils.store_reading(payload, topic, client)

        mock_write_points.assert_called()

    def test_store_readings_none_topic(self):

        payload = json.loads('{"time": "2022-01-01 00:00:00.000", "value": 123.456}')

        client = MagicMock()

        with patch.object(client, 'write_points') as mock_write_points:
            with self.assertRaises(AttributeError):
                db_utils.store_reading(payload, None, client)

    def test_store_readings_none_payload(self):
        topic = json.loads('{"location": "location_9000", "asset": "9000", "measurement": "operationPower"}')

        client = MagicMock()

        with patch.object(client, 'write_points') as mock_write_points:
            with self.assertRaises(AttributeError):
                db_utils.store_reading(None, topic, client)


class TestDBUtils(unittest.TestCase):
    # def test_db_conn_all_creds(self):
    #     client = db_utils.get_connection({"db_url":"edgeflex-persistance", "db_user":"admin", "db_pass":"admin", "db_port":8086, "db_name":"readings"})
    #     ready = client.ping()
    #     client.close()
    #     self.assertEqual("1.8.3", ready)

    def test_db_conn_null_creds(self):
        with self.assertRaises(TypeError):
            db_utils.get_connection()

