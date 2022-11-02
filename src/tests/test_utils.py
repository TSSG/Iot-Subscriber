import json
import unittest
import unittest.mock as mock
from datetime import datetime

from utils import validate, transform

class TestTransform(unittest.TestCase):
    def test_construct_data_item(self):
        data_item = json.loads('{"fields": {"time": "2022-10-07 00:00:00", "val_list_1_1": 123.456, "value": 123.456}, "time": "2022-10-07 00:00:00", "tags": {"location": "location_9000", "asset": "9000", "measurement": "operationPower"}, "measurement": "location_9000"}') 
        topic = json.loads('{"location": "location_9000", "asset": "9000", "measurement": "operationPower"}')
        payload = json.loads('{"time": "2022-10-07 00:00:00", "val_list": [[123.456]], "value": 123.456}')

        result = transform.construct_data_item(payload, topic)

        self.assertDictEqual(result, data_item)

    def test_construct_data_item_bad_time(self):
        tst_date = datetime.utcnow()
        topic = json.loads('{"location": "location_9000", "asset": "9000", "measurement": "operationPower"}')
        payload = json.loads('{"time": "2022-0 00:00:00.000", "val_list": [[123.456]], "value": 123.456}')

        result = transform.construct_data_item(payload, topic)

        self.assertTrue(result["time"] >= tst_date)

    def test_split_topic(self):
        topic = "location_27/27/operationPower"
        example = {"location": "location_27", "asset":"27", "measurement":"operationPower"}
        result = transform.split_topic(topic)
        self.assertDictEqual(example, result)



class TestValidate(unittest.TestCase):
    def test_validate(self):
        pload = {'fields': {'time': '2022-01-31T00:00:00Z', 'value': 0.0}, 'time': '2022-01-31 00:00:00+00:00', 'measurement': 'location_36'}
        topic = {'location': 'AGC', 'asset': 'device_vpp_agc_1', 'measurement': ''}
        
        result = validate.validate_data(pload, topic)

        self.assertEqual(pload, result)

    @mock.patch("utils.transform.construct_data_item")
    def test_validate_transformable(self, mock_parser):
        pload = {'mode': 'AGC', 'scenario': 'vpp_agc', 'time': 1643587200000000000, 'active_power': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'agc_ref': 0.0}
        topic = {'location': 'AGC', 'asset': 'device_vpp_agc_1', 'measurement': ''}
        
        validate.validate_data(pload, topic)

        mock_parser.assert_called_once_with(pload, topic)

    def test_validate_invalid_payload(self):
        pload = {'notakey': 'notavalue'}
        topic = {'location': 'AGC', 'asset': 'device_vpp_agc_1', 'measurement': ''}

        with self.assertRaises(KeyError):
            validate.validate_data(pload, topic)

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
