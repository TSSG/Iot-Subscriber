import unittest
import json
from unittest.mock import patch, MagicMock

from utils import db_utils


class TestStore(unittest.TestCase):
    def test_store_reading(self):
        payload = json.loads('{"fields": {"time": "2022-12-31T00:00:00Z", "value": 0.0}, "time": "2022-11-14 12:19:00+00:00", "tags": {"location": "location_36", "asset": "36", "measurement": "operationPower"}, "measurement": "location_36"}')

        client = MagicMock()

        with patch.object(client, 'write_points') as mock_write_points:
            db_utils.store_reading(payload, client)

        mock_write_points.assert_called()

    def test_store_reading_invalid_date(self):
        payload = json.loads('{"fields": {"time": "2022-1T00:00:00Z", "value": 0.0}, "time": "2022-12-31 00:00:00+00:00", "tags": {"location": "location_36", "asset": "36", "measurement": "operationPower"}, "measurement": "location_36"}')

        client = MagicMock()

        with patch.object(client, 'write_points') as mock_write_points:
            db_utils.store_reading(payload, client)

        mock_write_points.assert_called()

    def test_store_readings_none_payload(self):
        client = MagicMock()

        with patch.object(client, 'write_points') as mock_write_points:
            with self.assertRaises(TypeError):
                db_utils.store_reading(None, client)


class TestDBUtils(unittest.TestCase):
    def test_db_conn_null_creds(self):
        with self.assertRaises(TypeError):
            db_utils.get_connection()

    def test_get_dbs(self):
        client = MagicMock()
        client.get_list_database = MagicMock(return_value=[{"name": "database1"}, {"name": "database2"}])

        expected = ["database1", "database2"]
        result = db_utils.get_dbs(client)

        self.assertListEqual(expected, result)
