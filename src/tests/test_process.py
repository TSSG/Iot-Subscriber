import unittest
import unittest.mock as mock

import process


class TestProcess(unittest.TestCase):
    @mock.patch("db_utils.store_reading")
    @mock.patch("db_utils.get_dbs")
    def test_process(self, mock_dbs, mock_store):
        data = {"time": 1682060040000000000, "fields": {"value": 50}, "tags": {"location": "waterford"}}
        topic = "database1/measurement1"
        db_creds = {"db_url": "my-db", "db_user": "user", "db_pass": "pass", "db_port": 8086, "db_name": "readings"}

        mock_store.return_value = True
        mock_dbs.return_value = ["database1"]

        response = process.process_payload(data, topic, db_creds)

        self.assertEqual(response, 0)

    @mock.patch("db_utils.store_reading")
    @mock.patch("db_utils.get_dbs")
    def test_process_bad_db(self, mock_dbs, mock_store):
        data = {"time": 1682060040000000000, "fields": {"value": 50}, "tags": {"location": "waterford"}}
        topic = "database1/measurement1"
        db_creds = {"db_url": "my-db", "db_user": "user", "db_pass": "pass", "db_port": 8086, "db_name": "readings"}

        mock_dbs.return_value = ["database2"]

        response = process.process_payload(data, topic, db_creds)

        self.assertEqual(response, 1)

    @mock.patch("db_utils.store_reading")
    @mock.patch("db_utils.get_dbs")
    def test_process_bad_format(self, mock_dbs, mock_store):
        data = {"time": 1682060040000000000, "fields": {"value": 50}, "tags": {"location": "waterford"}}
        topic = "database1/measurement1"
        db_creds = {"db_url": "my-db", "db_user": "user", "db_pass": "pass", "db_port": 8086, "db_name": "readings"}

        mock_store.return_value = False
        mock_dbs.return_value = ["database1"]

        response = process.process_payload(data, topic, db_creds)

        self.assertEqual(response, 1)

    @mock.patch("db_utils.store_reading")
    @mock.patch("db_utils.get_dbs")
    def test_process_raised_exception(self, mock_dbs, mock_store):
        data = {"time": 1682060040000000000, "fields": {"value": 50}, "tags": {"location": "waterford"}}
        topic = "database1/measurement1"
        db_creds = {"db_url": "my-db", "db_user": "user", "db_pass": "pass", "db_port": 8086, "db_name": "readings"}

        mock_store.side_effect = KeyError()
        mock_dbs.return_value = ["database1"]

        response = process.process_payload(data, topic, db_creds)

        self.assertEqual(response, 1)

