import json
import unittest
import unittest.mock as mock

from rest import process_payload


class TestRest(unittest.TestCase):
    @mock.patch("utils.db_utils.store_reading")
    def test_process(self, mock_store):
        data = {'topic': 'database1/AGC/device_vpp_agc_1', 'payload': {'fields': {'time': 1663917144761711104, 'active_power_1': 0.0, 'active_power_2': 0.0, 'active_power_3': 0.0, 'active_power_4': 0.0, 'active_power_5': 0.0, 'active_power_6': 0.0, 'active_power_7': 0.0, 'active_power_8': 0.0, 'active_power_9': 0.0, 'active_power_10': 0.0, 'agc_ref': 0.0}, 'time': '2022-09-23 07:12:24.761711', 'measurement': 'AGC'}}
        dbs = ["database1", "database2"]
        db_creds = {"db_url": "my-db", "db_user": "user", "db_pass": "pass", "db_port": 8086, "db_name": "readings"}

        mock_store.return_value = True

        response = process_payload.process(data, dbs, db_creds)

        self.assertDictEqual(json.loads(response[0]), {"success": True, "Description": "Payload stored successfully."})
        self.assertEqual(response[1], 200)

    @mock.patch("utils.db_utils.store_reading")
    def test_process_bad_db(self, mock_store):
        data = {'topic': 'notadb/AGC/device_vpp_agc_1', 'payload': {'fields': {'time': 1663917144761711104, 'active_power_1': 0.0, 'active_power_2': 0.0, 'active_power_3': 0.0, 'active_power_4': 0.0, 'active_power_5': 0.0, 'active_power_6': 0.0, 'active_power_7': 0.0, 'active_power_8': 0.0, 'active_power_9': 0.0, 'active_power_10': 0.0, 'agc_ref': 0.0}, 'time': '2022-09-23 07:12:24.761711', 'measurement': 'AGC'}}
        dbs = ["database1", "database2"]
        db_creds = {"db_url": "my-db", "db_user": "user", "db_pass": "pass", "db_port": 8086, "db_name": "readings"}

        response = process_payload.process(data, dbs, db_creds)

        self.assertIn("database has not been created", response[0])
        self.assertEqual(response[1], 400)

    @mock.patch("utils.db_utils.store_reading")
    def test_process_bad_format(self, mock_store):
        data = {'payload': {'fields': {'time': 1663917144761711104, 'active_power_1': 0.0, 'active_power_2': 0.0, 'active_power_3': 0.0, 'active_power_4': 0.0, 'active_power_5': 0.0, 'active_power_6': 0.0, 'active_power_7': 0.0, 'active_power_8': 0.0, 'active_power_9': 0.0, 'active_power_10': 0.0, 'agc_ref': 0.0}, 'time': '2022-09-23 07:12:24.761711', 'measurement': 'AGC'}}
        dbs = ["database1", "database2"]
        db_creds = {"db_url": "my-db", "db_user": "user", "db_pass": "pass", "db_port": 8086, "db_name": "readings"}

        mock_store.return_value = True

        response = process_payload.process(data, dbs, db_creds)

        self.assertIn("Request is not in the required format.", response[0])
        self.assertEqual(response[1], 400)

    @mock.patch("utils.db_utils.store_reading")
    def test_process_raised_exception(self, mock_store):
        data = {'topic': 'database1/AGC/device_vpp_agc_1', 'payload': {'fields': {'time': 1663917144761711104, 'active_power_1': 0.0, 'active_power_2': 0.0, 'active_power_3': 0.0, 'active_power_4': 0.0, 'active_power_5': 0.0, 'active_power_6': 0.0, 'active_power_7': 0.0, 'active_power_8': 0.0, 'active_power_9': 0.0, 'active_power_10': 0.0, 'agc_ref': 0.0}, 'time': '2022-09-23 07:12:24.761711', 'measurement': 'AGC'}}
        dbs = ["database1", "database2"]
        db_creds = {"db_url": "my-db", "db_user": "user", "db_pass": "pass", "db_port": 8086, "db_name": "readings"}

        mock_store.side_effect = KeyError()

        response = process_payload.process(data, dbs, db_creds)

        self.assertIn("Bad Request", response[0])
        self.assertEqual(response[1], 400)

    @mock.patch("utils.db_utils.store_reading")
    def test_store_data(self, mock_store):
        client = mock.MagicMock()
        mock_store.return_value = True

        data = {'topic': 'AGC/device_vpp_agc_1/', 'payload': {"mode": "AGC ", "scenario": "vpp_agc", "time": 1663917144761711104, "active_power": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "agc_ref": 0.0}}
        valid_pload = {'fields': {'time': 1663917144761711104, 'active_power_1': 0.0, 'active_power_2': 0.0, 'active_power_3': 0.0, 'active_power_4': 0.0, 'active_power_5': 0.0, 'active_power_6': 0.0, 'active_power_7': 0.0, 'active_power_8': 0.0, 'active_power_9': 0.0, 'active_power_10': 0.0, 'agc_ref': 0.0}, 'time': '2022-09-23 07:12:24.761711', 'tags': {'location': 'AGC', 'asset': 'device_vpp_agc_1', 'measurement': '', 'mode': 'AGC ', 'scenario': 'vpp_agc'}, 'measurement': 'AGC'}
        topic = {'location': 'AGC', 'asset': 'device_vpp_agc_1', 'measurement': ''}

        summary, status_code = process_payload.store_data(data, client)

        mock_store.assert_called_once_with(valid_pload, topic, client)
        self.assertDictEqual(summary, {"success": True, "Description": "Payload stored successfully."})
        self.assertEqual(status_code, 200)

    @mock.patch("utils.db_utils.store_reading")
    def test_store_data_failed(self, mock_store):
        client = mock.MagicMock()
        mock_store.return_value = False

        data = {'topic': 'notadb', 'payload': {'fields': {'time': 1663917144761711104, 'active_power_1': 0.0, 'active_power_2': 0.0, 'active_power_3': 0.0, 'active_power_4': 0.0, 'active_power_5': 0.0, 'active_power_6': 0.0, 'active_power_7': 0.0, 'active_power_8': 0.0, 'active_power_9': 0.0, 'active_power_10': 0.0, 'agc_ref': 0.0}, 'time': '2022-09-23 07:12:24.761711', 'measurement': 'AGC'}}

        summary, status_code = process_payload.store_data(data, client)

        self.assertEqual(summary["success"], False)
        self.assertIn("Could not store payload", summary["Description"])
        self.assertEqual(status_code, 400)