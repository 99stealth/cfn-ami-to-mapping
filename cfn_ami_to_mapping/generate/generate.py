from cfn_ami_to_mapping.get import Get

class Generate:
    get_handler = Get
    def cfn_ami_mapping_section(self, initial_images_map, aws_regions, map_name, quiet_mode, aws_access_key_id, aws_secret_access_key):
        ''' Function receives initial images map, then goes withtheir names across all
         AWS regions and getting their ids. Function returns map with images per 
         region '''

        images_map = {}
        images_names = self.get_handler.images_names_from_init_name_map(initial_images_map)
        if not quiet_mode:
            print('[!] Generating mapping for you. Please, wait several seconds.')
        for region in aws_regions:
            region_image_map = {}
            client = self.get_handler.aws_client('ec2', region, aws_access_key_id, aws_secret_access_key)
            full_images_info = self.get_handler.images_info_by_name(client, images_names, quiet_mode)
            for image_map in initial_images_map:
                for image_info in full_images_info:
                    if initial_images_map[image_map]['image_name'] == image_info['Name']:
                        if region not in region_image_map:
                            region_image_map[region] = { image_map: image_info['ImageId'] }
                        else:
                            region_image_map[region][image_map] = image_info['ImageId']
            images_map.update(region_image_map)
        return {map_name: images_map}


    