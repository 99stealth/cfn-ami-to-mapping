import unittest

from cfn_ami_to_mapping import Transform


class TestTransform(unittest.TestCase):
    def setUp(self):
        self.transformation = Transform()

    def test_dictionary_to_json_with_simple_dictionary(self):
        test_data = {'key': 'value'}
        self.assertEquals(self.transformation.dictionary_to_json(test_data), ('{\n    "key": "value"\n}'))

    def test_dictionary_to_yaml_with_simple_dictionary(self):
        test_data = {'key': 'value'}
        self.assertEquals(self.transformation.dictionary_to_yaml(test_data), ('key: value\n'))


if __name__ == '__main__':
    unittest.main()
