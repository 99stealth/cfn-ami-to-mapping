#!/usr/bin/python

import argparse
import boto3
from botocore.exceptions import ClientError, ParamValidationError
import json
import yaml


def parse_arguments():
    parser = argparse.ArgumentParser(description='Create mapping for CloudFormation with AMIs by region',
                                    epilog='')
    output_format_group = parser.add_mutually_exclusive_group(required=False)
    output_format_group.add_argument('-j', '--json', action="store_true")   # make default if it is in ~/.aws/config
    output_format_group.add_argument('-y', '--yaml', action="store_true", default=True)   # make default if it is in ~/.aws/config
    ami_identifier_group = parser.add_mutually_exclusive_group(required=True)
    ami_identifier_group.add_argument('-i', '--image-id', action='append')
    ami_identifier_group.add_argument('-n', '--image-name', action='append')
    parser.add_argument('-m', '--map-name', default="AMIRegionMap")
    parser.add_argument('-k', '--top-level-key', action='append', required=True)
    parser.add_argument('-r', '--region', action='store', default='us-east-1')                 # make default if it is in ~/.aws/config

    args = parser.parse_args()

    if args.image_id:
        if len(args.image_id) != len(args.top_level_key):
            parser.error("Number of -i/--image-id should be equal to number of -k/--top-level-key")
    elif args.image_name:
        if len(args.image_name) != len(args.top_level_key):
            parser.error("Number of -n/--image-name should be equal to number of -k/--top-level-key")

    return args


def get_regions(client):
    try:
        return [region['RegionName'] for region in client.describe_regions()['Regions']]
    except ClientError as e:
        print('Unexpected error: {}'.format(e))
    except ParamValidationError as e:
        print('Parameter validation error: {}'.format(e))


def get_client(resource, region):
    try:
        return boto3.client(resource, region_name=region)
    except ClientError as e:
        print('Unexpected error: {}'.format(e))
    except ParamValidationError as e:
        print('Parameter validation error: {}'.format(e))


def enrich_images_info_with_id(full_images_info, initial_images_map_with_image_name):
    for image_map in initial_images_map_with_image_name:
        for image_info in full_images_info:
            if image_info['Name'] == initial_images_map_with_image_name[image_map]['image_name']:
                initial_images_map_with_image_name[image_map]['image_id'] = image_info['ImageId']
    return initial_images_map_with_image_name


def enrich_images_info_with_name(full_images_info, initial_images_map_with_image_id):
    for image_map in initial_images_map_with_image_id:
        for image_info in full_images_info:
            if image_info['ImageId'] == initial_images_map_with_image_id[image_map]['image_id']:
                initial_images_map_with_image_id[image_map]['image_name'] = image_info['Name']
    return initial_images_map_with_image_id


def get_images_ids_from_init_id_map(initial_images_map_with_image_id):
    return [initial_images_map_with_image_id[top_level_key]['image_id'] for top_level_key in initial_images_map_with_image_id]


def get_images_names_from_init_name_map(initial_images_map_with_image_name):
    return [initial_images_map_with_image_name[top_level_key]['image_name'] for top_level_key in initial_images_map_with_image_name]


def get_images_info_by_id(client, images_ids):
    try:
        response = client.describe_images(ImageIds=images_ids)
        return response['Images']
    except ClientError as e:
        print('Unexpected error: {}'.format(e))
    except ParamValidationError as e:
        print('Parameter validation error: {}'.format(e))


def get_images_info_by_name(client, images_names):
    try:
        response = client.describe_images(Filters=[
            {
                'Name': 'name',
                'Values': images_names
            },
            {
                'Name': 'state',
                'Values': [ 'available' ]
            }
        ],)
        return response['Images']
    except ClientError as e:
        print('Unexpected error: {}'.format(e))
    except ParamValidationError as e:
        print('Parameter validation error: {}'.format(e))


def parse_images_ids_from_info(images_info):
    images_ids = [ images['ImageId'] for images in images_info ]
    return images_ids


def parse_images_names_from_info(images_info):
    images_names = [ images['Name'] for images in images_info ]
    return images_names


def generate_map(initial_images_map, aws_regions, map_name):
    images_map = {}
    images_names = get_images_names_from_init_name_map(initial_images_map)
    for region in aws_regions:
        region_image_map = {}
        client = get_client('ec2', region)
        full_images_info = get_images_info_by_name(client, images_names)
        for image_map in initial_images_map:
            for image_info in full_images_info:
                if initial_images_map[image_map]['image_name'] == image_info['Name']:
                    if region not in region_image_map:
                        region_image_map[region] = { image_map: image_info['ImageId'] }
                    else:
                        region_image_map[region][image_map] = image_info['ImageId']
        images_map.update(region_image_map)
    return {map_name: images_map}


def dictionary_to_json(images_map):
    return json.dumps(images_map, indent=4, sort_keys=True)


def dictionary_to_yaml(images_map):
    return yaml.dump(images_map)


def main():
    args = parse_arguments()
    client = get_client('ec2', args.region)
    aws_regions = get_regions(client)
    if args.image_id:
        initial_images_map_with_image_id = {}
        iter = 0
        for top_level_key in args.top_level_key:
            initial_images_map_with_image_id[top_level_key] = { "image_id": args.image_id[iter] }
            iter = iter + 1
        images_ids = get_images_ids_from_init_id_map(initial_images_map_with_image_id)
        full_images_info = get_images_info_by_id(client, images_ids)
        initial_images_map = enrich_images_info_with_name(full_images_info, initial_images_map_with_image_id)
    elif args.image_name:
        initial_images_map_with_image_name = {}
        iter = 0
        for top_level_key in args.top_level_key:
            initial_images_map_with_image_name[top_level_key] = { "image_name": args.image_name[iter] }
            iter = iter + 1
        images_names = get_images_names_from_init_name_map(initial_images_map_with_image_name)
        full_images_info = get_images_info_by_name(client, images_names)
        initial_images_map = enrich_images_info_with_id(full_images_info, initial_images_map_with_image_name)
    images_map = generate_map(initial_images_map, aws_regions, args.map_name)
    if args.json:
        print(dictionary_to_json(images_map))
    elif args.yaml:
        print(dictionary_to_yaml(images_map))


if __name__ == '__main__':
    main()