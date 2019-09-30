import boto3
from botocore.exceptions import ClientError, ParamValidationError


class Get:
    def aws_client(self, resource, region, aws_access_key_id, aws_secret_access_key):
        ''' Method provides AWS client for resource in region which were passed
        to the function '''

        try:
            if aws_access_key_id and aws_secret_access_key:
                return boto3.client(resource, region_name=region, aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key)
            else:
                return boto3.client(resource, region_name=region)
        except ClientError as e:
            print('Unexpected error: {}'.format(e))
        except ParamValidationError as e:
            print('Parameter validation error: {}'.format(e))

    def aws_regions(self, client):
        ''' Method provides list of regions which are available for current
        account '''

        try:
            return [region['RegionName'] for region in client.describe_regions()['Regions']]
        except ClientError as e:
            print('Unexpected error: {}'.format(e))
        except ParamValidationError as e:
            print('Parameter validation error: {}'.format(e))

    def images_ids_from_init_id_map(self, initial_images_map_with_image_id):
        ''' Function receives initial map and returns all images ids from the
        received map '''

        return [initial_images_map_with_image_id[top_level_key]['image_id']
                for top_level_key in initial_images_map_with_image_id]

    def images_names_from_init_name_map(self, initial_images_map_with_image_name):
        ''' Function receives initial map and returns all images names from the
        received map '''

        return [initial_images_map_with_image_name[top_level_key]['image_name']
                for top_level_key in initial_images_map_with_image_name]

    def images_info_by_id(self, client, images_ids, quiet_mode):
        ''' Function receives images ids and returns all the related data '''

        if not quiet_mode:
            print('[!] Getting full info about image(s) {} in {}'.format(' '.join(images_ids), client.meta.region_name))
        try:
            response = client.describe_images(ImageIds=images_ids)
            return response['Images']
        except ClientError as e:
            print('Unexpected error: {}'.format(e))
        except ParamValidationError as e:
            print('Parameter validation error: {}'.format(e))

    def images_info_by_name(self, client, images_names, quiet_mode):
        ''' Function receives images names and returns all the related data '''

        if not quiet_mode:
            print('[!] Getting full info about image {} in {}'.format(' '.join(images_names), client.meta.region_name))
        try:
            response = client.describe_images(Filters=[
                {
                    'Name': 'name',
                    'Values': images_names
                },
                {
                    'Name': 'state',
                    'Values': ['available']
                }
            ],)
            return response['Images']
        except ClientError as e:
            print('Unexpected error: {}'.format(e))
        except ParamValidationError as e:
            print('Parameter validation error: {}'.format(e))
