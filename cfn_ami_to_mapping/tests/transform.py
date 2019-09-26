import unittest
from cfn_ami_to_mapping import Transform

class TestTransform(unittest.TestCase):
    def setUp(self):
        self.transformation = Transform()

    def test_dictionary_to_json_with_simple_dictionary(self):
        test_data = {'1': {'key': 'value'}, '2': {'key': 'value'}}
        self.assertEquals(self.transformation.dictionary_to_json(test_data), ('{\n    "1": {\n        "key": "value"\n    },\n    "2": {\n        "key": "value"\n    }\n}'))

    def test_dictionary_to_yaml_with_simple_dictionary(self):
        test_data = {'1': {'key': 'value'}, '2': {'key': 'value'}}
        self.assertEquals(self.transformation.dictionary_to_yaml(test_data), ("'1':\n  key: value\n'2':\n  key: value\n"))


if __name__ == '__main__':
    unittest.main()