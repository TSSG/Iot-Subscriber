import sys
import unittest
import unittest.mock as mock

sys.path.append("..")
import app


class TestRest(unittest.TestCase):

    def test_storage_request(self):
        m = mock.MagicMock()
        m.json = {'route': 'AGC', 'payload': {'fields': {'time': 1663917144761711104, 'active_power_1': 0.0, 'active_power_2': 0.0, 'active_power_3': 0.0, 'active_power_4': 0.0, 'active_power_5': 0.0, 'active_power_6': 0.0, 'active_power_7': 0.0, 'active_power_8': 0.0, 'active_power_9': 0.0, 'active_power_10': 0.0, 'agc_ref': 0.0}, 'time': '2022-09-23 07:12:24.761711', 'measurement': 'AGC'}}

        with mock.patch("app.request", m):
            summary, response_code, headers = app.storage_request()
            self.assertIn("POST successful", summary)
            self.assertEqual(response_code, 200)

    def test_storage_request_bad_db(self):
        m = mock.MagicMock()
        m.json = {'route': 'notadb', 'payload': {'fields': {'time': 1663917144761711104, 'active_power_1': 0.0, 'active_power_2': 0.0, 'active_power_3': 0.0, 'active_power_4': 0.0, 'active_power_5': 0.0, 'active_power_6': 0.0, 'active_power_7': 0.0, 'active_power_8': 0.0, 'active_power_9': 0.0, 'active_power_10': 0.0, 'agc_ref': 0.0}, 'time': '2022-09-23 07:12:24.761711', 'measurement': 'AGC'}}

        with mock.patch("app.request", m):
            summary, response_code, headers = app.storage_request()
            self.assertIn("database has not been created", summary)
            self.assertEqual(response_code, 400)

    def test_storage_request_bad_format(self):
        m = mock.MagicMock()
        m.json = "{'invalidjson:}{"

        with mock.patch("app.request", m):
            summary, response_code, headers = app.storage_request()
            self.assertIn("Bad Request", summary)
            self.assertEqual(response_code, 400)
