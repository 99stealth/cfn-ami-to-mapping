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

if __name__ == '__main__':
    unittest.main()