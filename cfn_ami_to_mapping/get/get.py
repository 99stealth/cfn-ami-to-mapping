import sys
import logging
import concurrent.futures
from itertools import repeat

import boto3
from botocore.exceptions import ClientError, ParamValidationError, EndpointConnectionError


class Get:
    def aws_client(self, resource, region, aws_access_key_id, aws_secret_access_key, check_client=False):
        ''' Method provides AWS client for resource in region which were passed
        to the function '''

        if aws_access_key_id and aws_secret_access_key:
            client = boto3.client(resource, region_name=region, aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key)
        else:
            client = boto3.client(resource, region_name=region)

        if check_client:
            try:
                if client.describe_id_format(Resource='image')['ResponseMetadata']['HTTPStatusCode'] == 200:
                    return client
            except EndpointConnectionError as e:
                logging.error('Region {} is unavailable or does not exist. {}'.format(region, e))
                sys.exit(1)
            except ClientError as e:
                logging.error('Unexpected error: {}'.format(e))
                sys.exit(1)
            except ParamValidationError as e:
                logging.error('Parameter validation error: {}'.format(e))
                sys.exit(1)
        else:
            return client

    def aws_clients_in_all_regions(self, aws_regions, aws_access_key_id, aws_secret_access_key):
        ''' Method provides aws clients for all AWS regions '''

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.aws_client, repeat('ec2'), aws_regions,
                                   repeat(aws_access_key_id), repeat(aws_secret_access_key))
            clients = [result for result in results]
        return dict(zip(aws_regions, clients))

    def aws_regions(self, client):
        ''' Method provides list of regions which are available for current
        account '''

        try:
            return [region['RegionName'] for region in client.describe_regions()['Regions']]
        except ClientError as e:
            logging.error('Unexpected error: {}'.format(e))
            sys.exit(1)
        except ParamValidationError as e:
            logging.error('Parameter validation error: {}'.format(e))
            sys.exit(1)

    def aws_regions_after_exclude(self, aws_regions, aws_regions_to_exclude):
        ''' Method provides list of aws regions after eliminating unnecessary ones '''

        for region in aws_regions_to_exclude:
            aws_regions.remove(region)
        return aws_regions

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

    def images_info_by_id(self, client, images_ids):
        ''' Function receives images ids and returns all the related data '''

        logging.info('Getting full info about image(s) {} in {}'.format(' '.join(images_ids), client.meta.region_name))
        try:
            response = client.describe_images(ImageIds=images_ids)
            return response['Images']
        except ClientError as e:
            logging.error('Unexpected error: {}'.format(e))
            sys.exit(1)
        except ParamValidationError as e:
            logging.error('Parameter validation error: {}'.format(e))
            sys.exit(1)

    def images_info_by_name(self, client, region, images_names):
        ''' Function receives images names and returns all the related data '''

        if type(client) is dict:
            client = client[region]
        logging.info('Getting full info about image(s) {} in {}'.format(' '.join(images_names),
                                                                        client.meta.region_name))
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
            logging.error('Unexpected error: {}'.format(e))
            sys.exit(1)
        except ParamValidationError as e:
            logging.error('Parameter validation error: {}'.format(e))
            sys.exit(1)
