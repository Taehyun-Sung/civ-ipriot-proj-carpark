import unittest
import json
from smartpark.config_parser import parse_config


class TestConfigParsing(unittest.TestCase):
    def test_parse_config_has_correct_location_and_spaces(self):
        config_string = '''
        {
            "parking_lot": {
                "location": "raf-park-international",
                "total_spaces": 130,
                "broker_host": "localhost",
                "broker_port": 1883
            }
        }
        '''

        config = json.loads(config_string)
        parking_lot = parse_config(config)
        self.assertEqual(parking_lot['location'], "raf-park-international")
        self.assertEqual(parking_lot['total_spaces'], 130)