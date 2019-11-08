import argparse
import logging
import sys

from cfn_ami_to_mapping import Enrich, Generate, Get, Transform, Validate
from cfn_ami_to_mapping._version import __version__


def parse_arguments():
    ''' Function allows to parse arguments from the line input and check if all
    of them are entered correctly '''

    cfn_ami_to_mapping_validate = Validate()
    parser = argparse.ArgumentParser(
        description='Create mapping for CloudFormation with AMIs by region',
        epilog='Find more at https://github.com/99stealth/cfn-ami-to-mapping'
    )
    output_format_group = parser.add_mutually_exclusive_group(required=False)
    output_format_group.add_argument('-j', '--json', action='store_true',
                                     help='Sets output format to json. Cannot be used with --yaml')
    output_format_group.add_argument('-y', '--yaml', action='store_true', default=True,
                                     help='Sets output format to yaml. Cannot be used with --json')
    ami_identifier_group = parser.add_mutually_exclusive_group(required=True)
    ami_identifier_group.add_argument('-i', '--image-id', action='append', help='AWS image id, like i-00000000')
    ami_identifier_group.add_argument('-n', '--image-name', action='append', help='AWS image name')
    regions = parser.add_mutually_exclusive_group(required=False)
    regions.add_argument('--aws-regions', action='store', nargs='*',
                         help='Regions which you want to see in mapping')
    regions.add_argument('--aws-regions-exclude', action='store', nargs='*',
                         help='Regions which don\'t you want to see in mapping')
    parser.add_argument('--aws-access-key-id', action='store', help='AWS Access Key ID')
    parser.add_argument('--aws-secret-access-key', action='store', help='AWS Secret Access Key')
    parser.add_argument('-m', '--map-name', default='AMIRegionMap', help='Mapping\'s name (default: AMIRegionMap)')
    parser.add_argument('-k', '--top-level-key', action='append', required=True, help='Top Level Key')
    parser.add_argument('-r', '--region', action='store', default='us-east-1', help='AWS Region (default: us-east-1)')
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
                        help='Quiet mode doesn\'t show detailed output (default: False)')
    parser.add_argument('--version', action='version',
                        version='%(prog)s \033[0;32m{version}\033[0;0m'.format(version=__version__))

    args = parser.parse_args()

    if args.aws_access_key_id and args.aws_secret_access_key:
        if not args.quiet:
            print('''[!] You have provided your aws_access_key_id and aws_secret_access_key inline which is insecure.
                  Use \033[1maws configure\033[0m command to configure your''')
        if not cfn_ami_to_mapping_validate.aws_access_key_id(args.aws_access_key_id):
            print('[-] Provided AWS Access Key ID is not valid')
            sys.exit(1)
        elif not cfn_ami_to_mapping_validate.aws_secret_access_key(args.aws_secret_access_key):
            print('[-] Provided AWS Access Secret Key is not valid')
            sys.exit(1)

    elif args.aws_access_key_id and not args.aws_secret_access_key:
        parser.error('Parameter --aws-access-key-id requires --aws-secret-access-key')
    elif not args.aws_access_key_id and args.aws_secret_access_key:
        parser.error('Parameter --aws-secret-access-key requires --aws-access-key-id')

    if args.image_id:
        if len(args.image_id) != len(args.top_level_key):
            parser.error('Number of -i/--image-id should be equal to number of -k/--top-level-key')
    elif args.image_name:
        if len(args.image_name) != len(args.top_level_key):
            parser.error('Number of -n/--image-name should be equal to number of -k/--top-level-key')

    return args


def main():
    ''' Main function provides communication between all other functions '''

    cfn_ami_to_mapping_get = Get()
    cfn_ami_to_mapping_validate = Validate()
    cfn_ami_to_mapping_enrich = Enrich()
    cfn_ami_to_mapping_generate = Generate()
    cfn_ami_to_mapping_transform = Transform()

    args = parse_arguments()
    client = cfn_ami_to_mapping_get.aws_client('ec2', args.region, args.aws_access_key_id, args.aws_secret_access_key)
    aws_regions = cfn_ami_to_mapping_get.aws_regions(client)
    if args.aws_regions:
        regions_valid, invalid_region = cfn_ami_to_mapping_validate.aws_regions(aws_regions, args.aws_regions)
        if not regions_valid:
            print('[-] Invalid region {}'.format(invalid_region))
            sys.exit(1)
        else:
            aws_regions = args.aws_regions
    elif args.aws_regions_exclude:
        regions_valid, invalid_region = cfn_ami_to_mapping_validate.aws_regions(aws_regions, args.aws_regions_exclude)
        if not regions_valid:
            print('[-] Invalid region {}'.format(invalid_region))
            sys.exit(1)
        else:
            aws_regions = cfn_ami_to_mapping_get.aws_regions_after_exclude(aws_regions, args.aws_regions_exclude)

    if args.image_id:
        images_are_valid, incorrect_image_id = cfn_ami_to_mapping_validate.images_ids(args.image_id)
        if not images_are_valid:
            print("[-] Invalid image id {}".format(incorrect_image_id))
            sys.exit(1)
        initial_images_map_with_image_id = {}
        i = 0
        for top_level_key in args.top_level_key:
            initial_images_map_with_image_id[top_level_key] = {"image_id": args.image_id[i]}
            i = i + 1
        images_ids = cfn_ami_to_mapping_get.images_ids_from_init_id_map(initial_images_map_with_image_id)
        full_images_info = cfn_ami_to_mapping_get.images_info_by_id(client, images_ids, args.quiet)
        initial_images_map = cfn_ami_to_mapping_enrich.images_info_with_name(full_images_info,
                                                                             initial_images_map_with_image_id
                                                                             )
    elif args.image_name:
        initial_images_map_with_image_name = {}
        i = 0
        for top_level_key in args.top_level_key:
            initial_images_map_with_image_name[top_level_key] = {"image_name": args.image_name[i]}
            i = i + 1
        images_names = cfn_ami_to_mapping_get.images_names_from_init_name_map(initial_images_map_with_image_name)
        full_images_info = cfn_ami_to_mapping_get.images_info_by_name(client, args.region, images_names, args.quiet)
        initial_images_map = cfn_ami_to_mapping_enrich.images_info_with_id(full_images_info,
                                                                           initial_images_map_with_image_name
                                                                           )
    images_map = cfn_ami_to_mapping_generate.cfn_ami_mapping_section(initial_images_map,
                                                                     aws_regions,
                                                                     args.map_name,
                                                                     args.quiet,
                                                                     args.aws_access_key_id,
                                                                     args.aws_secret_access_key
                                                                     )
    if args.json:
        print(cfn_ami_to_mapping_transform.dictionary_to_json(images_map))
    elif args.yaml:
        print(cfn_ami_to_mapping_transform.dictionary_to_yaml(images_map))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("[-] Processing has been stopped. Interrupted by user")
        sys.exit(1)
