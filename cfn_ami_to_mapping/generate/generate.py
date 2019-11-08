import concurrent.futures
from itertools import repeat

from cfn_ami_to_mapping import Get


class Generate:
    def cfn_ami_mapping_section(self, initial_images_map, aws_regions, map_name, quiet_mode, aws_access_key_id,
                                aws_secret_access_key):
        ''' Function receives initial images map, then goes withtheir names across all
         AWS regions and getting their ids. Function returns map with images per
         region '''
        cfn_ami_to_mapping_get = Get()
        images_map = {}
        images_names = cfn_ami_to_mapping_get.images_names_from_init_name_map(initial_images_map)
        client_per_region = cfn_ami_to_mapping_get.aws_clients_in_all_regions(aws_regions,
                                                                              aws_access_key_id,
                                                                              aws_secret_access_key)
        if not quiet_mode:
            print('[!] Generating mapping for you. Please, wait several seconds.')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(cfn_ami_to_mapping_get.images_info_by_name,
                                   repeat(client_per_region),
                                   aws_regions,
                                   repeat(images_names),
                                   repeat(quiet_mode))
            full_images_info = [r for r in results]
        region_images_map = dict(zip(aws_regions, full_images_info))
        for region in region_images_map:
            image_map_by_region = {}
            for image_info in region_images_map[region]:
                for image_map in initial_images_map:
                    if initial_images_map[image_map]['image_name'] == image_info['Name']:
                        image_map_by_region[image_map] = image_info['ImageId']
            images_map[region] = image_map_by_region

        return {map_name: images_map}
