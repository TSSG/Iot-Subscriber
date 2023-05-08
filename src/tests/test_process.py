import json
import unittest
import unittest.mock as mock
from datetime import datetime

import process


class TestProcess(unittest.TestCase):
    @mock.patch("db_utils.store_reading")
    def test_process(self, mock_store):
        data = {"time": 1682060040000000000, "fields": {"value": 50}, "tags": {"location": "waterford"}}
        topic = "database1/measurement1"
        db_creds = {"url": "my-url", "org": "my-org", "token": "my-token"}

        mock_store.return_value = True

        response = process.process_payload(data, topic, db_creds)

        self.assertEqual(response, 0)

    @mock.patch("db_utils.store_reading")
    def test_process_bad_format(self, mock_store):
        data = {"time": 1682060040000000000, "fields": {"value": 50}, "tags": {"location": "waterford"}}
        topic = "database1/measurement1"
        db_creds = {"url": "my-url", "org": "my-org", "token": "my-token"}

        mock_store.side_effect = Exception()

        response = process.process_payload(data, topic, db_creds)

        self.assertEqual(response, 1)

    @mock.patch("db_utils.store_reading")
    def test_process_raised_exception(self, mock_store):
        data = {"time": 1682060040000000000, "fields": {"value": 50}, "tags": {"location": "waterford"}}
        topic = "database1/measurement1"
        db_creds = {"db_url": "my-db", "db_user": "user", "db_pass": "pass", "db_port": 8086, "db_name": "readings"}

        mock_store.side_effect = KeyError()

        response = process.process_payload(data, topic, db_creds)

        self.assertEqual(response, 1)


class TestTransform(unittest.TestCase):
    def test_construct_data_item(self):
        data_item = {"fields": {"value": 50, "val_list_1": 60, "val_list_2": 70, "val_list_3": 80}, "tags": {"location": "ireland"}, "time": 1682060040000000000, "measurement": "measurement1"}
        payload = {"time": 1682060040000000000, "value": 50, "val_list": [60, 70, 80], "location": "ireland", "measurement": "measurement1"}
        tags = ["location"]

        result = process.construct_data_item(payload, tags)

        self.assertDictEqual(result, data_item)


class TestValidate(unittest.TestCase):
    def test_validate(self):
        pload = {'fields': {'value': 0.0}, 'time': '2022-12-31 00:00:00+00:00', 'measurement': 'location_36'}
        tags = []

        result = process.validate_data(pload, tags)

        self.assertEqual(pload, result)

    @mock.patch("process.construct_data_item")
    def test_validate_transformable(self, mock_parser):
        pload = {"time": 1682060040000000000, "value": 50, "val_list": [60, 70, 80], "tag1": "waterford", "measurement": "measurement1"}
        tags = []

        process.validate_data(pload, tags)

        mock_parser.assert_called_once_with(pload, tags)

    def test_validate_invalid_payload(self):
        pload = {'notakey': 'notavalue'}
        tags = []

        with self.assertRaises(KeyError):
            process.validate_data(pload, tags)