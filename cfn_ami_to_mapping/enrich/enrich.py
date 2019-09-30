class Enrich:

    def images_info_with_id(self, full_images_info, initial_images_map_with_image_name):
        ''' Function enriches image info by its id and returns a result back '''

        for image_map in initial_images_map_with_image_name:
            for image_info in full_images_info:
                if image_info['Name'] == initial_images_map_with_image_name[image_map]['image_name']:
                    initial_images_map_with_image_name[image_map]['image_id'] = image_info['ImageId']
        return initial_images_map_with_image_name

    def images_info_with_name(self, full_images_info, initial_images_map_with_image_id):
        ''' Function enriches image info by its name and returns a result back '''

        for image_map in initial_images_map_with_image_id:
            for image_info in full_images_info:
                if image_info['ImageId'] == initial_images_map_with_image_id[image_map]['image_id']:
                    initial_images_map_with_image_id[image_map]['image_name'] = image_info['Name']
        return initial_images_map_with_image_id
