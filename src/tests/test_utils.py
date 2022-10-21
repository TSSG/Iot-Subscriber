import unittest
import unittest.mock as mock
from datetime import datetime

from utils import validate


class TestValidate(unittest.TestCase):
    def test_validate(self):
        pload = {'fields': {'time': '2022-01-31T00:00:00Z', 'value': 0.0}, 'time': '2022-01-31 00:00:00+00:00', 'measurement': 'location_36'}
        result = validate.validate_data(pload)

        self.assertEqual(pload, result)

    @mock.patch("utils.parsers.transform_data")
    def test_validate_transformable(self, mock_parser):
        pload = {'mode': 'AGC', 'scenario': 'vpp_agc', 'time': 1643587200000000000, 'active_power': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'agc_ref': 0.0}
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
