import unittest
from cfn_ami_to_mapping import Get


class TestGet(unittest.TestCase):
    def setUp(self):
        self.get = Get()

    def test_images_ids_from_init_id_map_with_one_image(self):
        test_data = {'AMIID': {'image_id': 'ami-035b3c7efe6d061d5'}}
        self.assertListEqual(self.get.images_ids_from_init_id_map(test_data), ['ami-035b3c7efe6d061d5'])

    def test_images_ids_from_init_id_map_with_two_image(self):
        test_data = {'AMIID': {'image_id': 'ami-035b3c7efe6d061d5'}, 'AMIID2': {'image_id': 'ami-0b898040803850657'}}
        ### Sorted is acceptable here since code is written in a way that order doesn't metter here
        self.assertListEqual(sorted(self.get.images_ids_from_init_id_map(test_data)), sorted(['ami-035b3c7efe6d061d5', 'ami-0b898040803850657']))

    def test_images_names_from_init_name_map_with_one_image(self):
        test_data = {'AMIID': {'image_name': 'amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2'}}
        self.assertListEqual(self.get.images_names_from_init_id_map(test_data), ['amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2'])

    def test_images_names_from_init_name_map_with_one_image(self):
        test_data = {'AMIID': {'image_name': 'amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2'}, 'AMIID2': {'image_name': 'amzn2-ami-hvm-2.0.20190618-x86_64-gp2'}}
        ### Sorted is acceptable here since code is written in a way that order doesn't metter here
        self.assertListEqual(sorted(self.get.images_names_from_init_name_map(test_data)), sorted(['amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2', 'amzn2-ami-hvm-2.0.20190618-x86_64-gp2']))

if __name__ == '__main__':
    unittest.main()