import json
import unittest
import unittest.mock as mock
from datetime import datetime

import validate
import transform


class TestTransform(unittest.TestCase):
    def test_construct_data_item(self):
        data_item = json.loads('{"fields": {"value": 50, "val_list_1": 60, "val_list_2": 70, "val_list_3": 80}, "tags": {}, "time": "2023-04-21 06:54:00", "measurement": "measurement1"}') 
        payload = json.loads('{"time": 1682060040000000000, "value": 50, "val_list": [60, 70, 80], "measurement": "measurement1"}')

        result = transform.construct_data_item(payload)

        self.assertDictEqual(result, data_item)

    def test_construct_data_item_bad_time(self):
        tst_date = datetime.utcnow()
        payload = json.loads('{"time": "2022-0 00:00:00.000", "val_list": [[123.456]], "value": 123.456}')

        result = transform.construct_data_item(payload)

        self.assertTrue(result["time"] >= tst_date)


class TestValidate(unittest.TestCase):
    def test_validate(self):
        pload = {'fields': {'value': 0.0}, 'time': '2022-12-31 00:00:00+00:00', 'measurement': 'location_36'}

        result = validate.validate_data(pload)

        self.assertEqual(pload, result)

    @mock.patch("transform.construct_data_item")
    def test_validate_transformable(self, mock_parser):
        pload = {"time": 1682060040000000000, "value": 50, "val_list": [60, 70, 80], "tag1": "waterford", "measurement": "measurement1"}

        validate.validate_data(pload)

        mock_parser.assert_called_once_with(pload)

    def test_validate_invalid_payload(self):
        pload = {'notakey': 'notavalue'}

        with self.assertRaises(KeyError):
            validate.validate_data(pload)

    def test_aleady_utc(self):
        time = "2022-07-10 00:00:00.000"
        time_parsed = validate.resolve_time(time)
        self.assertEqual(time_parsed, "2022-07-10 00:00:00")

    def test_not_full_utc(self):
        time = "2022-1 00:00:00.000"
        tst_date = datetime.utcnow()
        tm = validate.resolve_time(time)
        self.assertGreaterEqual(tm, tst_date)

    def test_already_utc_with_Z(self):
        time ="2022-06-27T14:33:00Z"
        time_parsed = validate.resolve_time(time)
        self.assertEqual(time_parsed, "2022-06-27 14:33:00+00:00")

    def test_unix(self):
        time = '1660654123841009152'
        time_parsed = validate.resolve_time(time)
        self.assertEqual(time_parsed, "2022-08-16 12:48:43.841009")

    def test_ddmmyy(self):
        time = '12-11-2022'
        time_parsed = validate.resolve_time(time)
        self.assertEqual(time_parsed, "2022-11-12 00:00:00")

    def test_unparsable_date(self):
        time = '1900-11-1010'
        tst_date = datetime.utcnow()
        tm = validate.resolve_time(time)
        self.assertGreaterEqual(tm, tst_date)

    def test_ISO(self):
        time = "2022-1 00:00:00.000"
        res = validate.validate_iso8601(time)
        self.assertFalse(res)

    def test_ISO_full_ISO(self):
        time = "2022-01-01 00:00:00.000"
        res = validate.validate_iso8601(time)
        self.assertTrue(res)

    def test_ISO_full_ISO_with_T(self):
        time = "2022-01-01T00:00:00.000"
        res = validate.validate_iso8601(time)
        self.assertTrue(res)

    def test_ISO_today(self):
        today = datetime.now()
        iso_date = today.isoformat()
        res = validate.validate_iso8601(iso_date)
        self.assertTrue(res)

    def test_ISO_NYE(self):
        time = "2022-12-31 23:59:59.999"
        res = validate.validate_iso8601(time)
        self.assertTrue(res)             

    def test_ddmmyyyy(self):
        time = '12-11-2022'
        self.assertTrue(validate.validate_ddmmyy(time))

    def test_ddmmyyyy(self):
        time = '12-11-2'
        self.assertFalse(validate.validate_ddmmyy(time))
