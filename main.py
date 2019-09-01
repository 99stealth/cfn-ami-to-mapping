#!/usr/bin/python

import argparse
import boto3
import json
import yaml


def parse_arguments():
    parser = argparse.ArgumentParser(description='Create mapping for CloudFormation with AMIs by region',
                                    epilog='')
    output_format_group = parser.add_mutually_exclusive_group(required=False)
    output_format_group.add_argument('-j', '--json', action="store_true")   # make default if it is in ~/.aws/config
    output_format_group.add_argument('-y', '--yaml', action="store_true")   # make default if it is in ~/.aws/config
    ami_identifier_group = parser.add_mutually_exclusive_group(required=True)
    ami_identifier_group.add_argument('-i', '--image-id', action='append')
    ami_identifier_group.add_argument('-n', '--image-name', action='append')
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
    return [region['RegionName'] for region in client.describe_regions()['Regions']]

def get_client(resource, region):
    return boto3.client(resource, region_name=region)

def get_images_info_by_id(client, images_ids):
    response = client.describe_images(ImageIds=images_ids)
    return response['Images']

def get_images_info_by_name(client, images_names):
    response = client.describe_images(Filters=[
        {
            'Name': 'Name',
            'Values': images_names
        },
        {
            'Name': 'state',
            'Values': [ 'available' ]
        }
    ],)
    return response['Images']

def parse_images_ids_from_info(images_info):
    images_ids = [ images['ImageId'] for images in images_info ]
    return images_ids

def parse_images_names_from_info(images_info):
    images_names = [ images['Name'] for images in images_info ]
    return images_names

def generate_map(images_names, top_level_keys, aws_regions):
    for region in aws_regions:
        client = get_client('ec2', region)
        print (region, client)

def main():
    args = parse_arguments()
    client = get_client('ec2', args.region)
    aws_regions = get_regions(client)
    if args.image_id:
        images_info = get_images_info_by_id(client, args.image_id)
        images_names = parse_images_names_from_info(images_info)
    elif args.image_name:
        images_names = args.image_name[:]
    images_map = generate_map(images_names, args.top_level_key, aws_regions)
    
        

if __name__ == '__main__':
    main()