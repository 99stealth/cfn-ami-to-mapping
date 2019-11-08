import unittest

from cfn_ami_to_mapping import Enrich


class TestEnrich(unittest.TestCase):
    def setUp(self):
        self.enrich = Enrich()

    def test_images_info_with_name_with_one_image(self):
        full_images_info_test_data = [{'Name': 'amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2',
                                       'ImageId': 'ami-035b3c7efe6d061d5'}]
        initial_images_map_with_image_id_test_data = {'AMIID': {'image_id': 'ami-035b3c7efe6d061d5'}}
        expected_output = {
                            'AMIID': {
                                'image_id': 'ami-035b3c7efe6d061d5',
                                'image_name': 'amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2'
                            }
                        }
        self.assertDictEqual(self.enrich.images_info_with_name(full_images_info_test_data,
                                                               initial_images_map_with_image_id_test_data
                                                               ), expected_output)

    def test_images_info_with_id_with_one_image(self):
        full_images_info_test_data = [{'Name': 'amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2',
                                       'ImageId': 'ami-035b3c7efe6d061d5'}]
        initial_images_map_with_image_name_test_data = {
                                                         'AMIID': {
                                                           'image_name': 'amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2'
                                                         }
                                                       }
        expected_output = {
                            'AMIID': {
                              'image_id': 'ami-035b3c7efe6d061d5',
                              'image_name': 'amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2'
                            }
                          }
        self.assertDictEqual(self.enrich.images_info_with_id(full_images_info_test_data,
                                                             initial_images_map_with_image_name_test_data
                                                             ), expected_output)

    def test_images_info_with_name_with_two_images(self):
        full_images_info_test_data = [
                                       {
                                           'Name': 'amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2',
                                           'ImageId': 'ami-035b3c7efe6d061d5'
                                       },
                                       {
                                           'Name': 'amzn2-ami',
                                           'ImageId': 'ami-00000000'
                                       }
                                      ]
        initial_images_map_with_image_id_test_data = {
                                                       'AMIID': {
                                                          'image_id': 'ami-035b3c7efe6d061d5'
                                                       },
                                                       'AMIID2': {
                                                          'image_id': 'ami-00000000'
                                                       }
                                                    }
        expected_output = {
                            'AMIID': {
                              'image_id': 'ami-035b3c7efe6d061d5',
                              'image_name': 'amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2'
                            },
                            'AMIID2': {
                              'image_id': 'ami-00000000',
                              'image_name': 'amzn2-ami'
                            }
                          }
        self.assertDictEqual(self.enrich.images_info_with_name(full_images_info_test_data,
                                                               initial_images_map_with_image_id_test_data
                                                               ), expected_output)

    def test_images_info_with_id_with_two_images(self):
        full_images_info_test_data = [
                                        {
                                          'Name': 'amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2',
                                          'ImageId': 'ami-035b3c7efe6d061d5'
                                        },
                                        {
                                          'Name': 'amzn2-ami',
                                          'ImageId': 'ami-00000000'
                                        }
                                      ]
        initial_images_map_with_image_name_test_data = {
                                                         'AMIID': {
                                                           'image_name': 'amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2'
                                                         },
                                                         'AMIID2': {
                                                           'image_name': 'amzn2-ami'
                                                         }
                                                       }
        expected_output = {
                            'AMIID': {
                              'image_id': 'ami-035b3c7efe6d061d5',
                              'image_name': 'amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2'
                            },
                            'AMIID2': {
                              'image_id': 'ami-00000000',
                              'image_name': 'amzn2-ami'
                            }
                          }
        self.assertDictEqual(self.enrich.images_info_with_id(full_images_info_test_data,
                                                             initial_images_map_with_image_name_test_data
                                                             ), expected_output)


if __name__ == '__main__':
    unittest.main()
