import unittest
from cfn_ami_to_mapping import Validate


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.validation = Validate()

    def test_images_ids_with_one_valid_17_char_image_id(self):
        self.assertEquals(self.validation.images_ids(['ami-00000000000000000']), (True, None))

    def test_images_ids_with_one_invalid_17_char_image_id(self):
        self.assertEquals(self.validation.images_ids(['ami-0000000000000000z']), (False, 'ami-0000000000000000z'))

    def test_images_ids_with_one_valid_8_char_image_id(self):
        self.assertEquals(self.validation.images_ids(['ami-00000000']), (True, None))

    def test_images_ids_with_one_invalid_8_char_image_id(self):
        self.assertEquals(self.validation.images_ids(['ami-0000000z']), (False, 'ami-0000000z'))

    def test_aws_access_key_id_with_valid_value(self):
        self.assertTrue(self.validation.aws_access_key_id('AKIAAAAAAAAAAAAAAAAA'))

    def test_aws_access_key_id_with_invalid_value(self):
        self.assertFalse(self.validation.aws_access_key_id('AKIAAAAAAAAAAAAAAAA'))

    def test_aws_secret_access_key_with_valid_value(self):
        self.assertTrue(self.validation.aws_secret_access_key('Aa1Aa0az00+AzA/01AzZZZz0Z0z0ZzzZZzZZz0zZ'))

    def test_aws_secret_access_key_with_invalid_value(self):
        self.assertFalse(self.validation.aws_secret_access_key('0ZzzZZzZZz0zZ'))


if __name__ == '__main__':
    unittest.main()
