import argparse
from cfn_ami_to_mapping import Get
from cfn_ami_to_mapping import Validate
from cfn_ami_to_mapping import Enrich
from cfn_ami_to_mapping import Generate
from cfn_ami_to_mapping import Transform

def parse_arguments():
    ''' Function allows to parse arguments from the line input and check if all
    of them are entered correctly '''

    parser = argparse.ArgumentParser(description='Create mapping for CloudFormation with AMIs by region',
                                    epilog='')
    output_format_group = parser.add_mutually_exclusive_group(required=False)
    output_format_group.add_argument('-j', '--json', action="store_true")
    output_format_group.add_argument('-y', '--yaml', action="store_true", default=True)
    ami_identifier_group = parser.add_mutually_exclusive_group(required=True)
    ami_identifier_group.add_argument('-i', '--image-id', action='append')
    ami_identifier_group.add_argument('-n', '--image-name', action='append')
    parser.add_argument('--aws-access-key-id', action='store')
    parser.add_argument('--aws-secret-access-key', action='store')
    parser.add_argument('-m', '--map-name', default="AMIRegionMap")
    parser.add_argument('-k', '--top-level-key', action='append', required=True)
    parser.add_argument('-r', '--region', action='store', default='us-east-1')
    parser.add_argument('-q', '--quiet', action='store_true', default=False)
    parser.add_argument('--version', action='version', version='%(prog)s 0.5.4')

    args = parser.parse_args()

    if args.aws_access_key_id and args.aws_secret_access_key and not args.quiet:
        print("[!] You have provided your aws_access_key_id and aws_secret_access_key inline which is insecure. Use \033[1maws configure\033[0m command to configure your ")
    elif args.aws_access_key_id and not args.aws_secret_access_key:
        parser.error("Parameter --aws-access-key-id requires --aws-secret-access-key")
    elif not args.aws_access_key_id and args.aws_secret_access_key:
        parser.error("Parameter --aws-secret-access-key requires --aws-access-key-id")


    if args.image_id:
        if len(args.image_id) != len(args.top_level_key):
            parser.error("Number of -i/--image-id should be equal to number of -k/--top-level-key")
    elif args.image_name:
        if len(args.image_name) != len(args.top_level_key):
            parser.error("Number of -n/--image-name should be equal to number of -k/--top-level-key")

    return args

def main():
    ''' Main fucntion provides communication between all other functions '''
    cfn_ami_to_mapping_get = Get()
    cfn_ami_to_mapping_validate = Validate()
    cfn_ami_to_mapping_enrich = Enrich()
    cfn_ami_to_mapping_generate = Generate()
    cfn_ami_to_mapping_transform = Transform()

    args = parse_arguments()
    client = cfn_ami_to_mapping_get.aws_client('ec2', args.region, args.aws_access_key_id, args.aws_secret_access_key)
    aws_regions = cfn_ami_to_mapping_get.aws_regions(client)
    if args.image_id:
        images_are_valid, incorrect_image_id = cfn_ami_to_mapping_validate.images_ids(args.image_id)
        if not images_are_valid:
            print("[-] Invalid image id {}".format(incorrect_image_id))
            exit(1)
        initial_images_map_with_image_id = {}
        iter = 0
        for top_level_key in args.top_level_key:
            initial_images_map_with_image_id[top_level_key] = { "image_id": args.image_id[iter] }
            iter = iter + 1
        images_ids = cfn_ami_to_mapping_get.images_ids_from_init_id_map(initial_images_map_with_image_id)
        full_images_info = cfn_ami_to_mapping_get.images_info_by_id(client, images_ids, args.quiet)
        initial_images_map = cfn_ami_to_mapping_enrich.images_info_with_name(full_images_info, initial_images_map_with_image_id)
    elif args.image_name:
        initial_images_map_with_image_name = {}
        iter = 0
        for top_level_key in args.top_level_key:
            initial_images_map_with_image_name[top_level_key] = { "image_name": args.image_name[iter] }
            iter = iter + 1
        images_names = cfn_ami_to_mapping_get.images_names_from_init_name_map(initial_images_map_with_image_name)
        full_images_info = cfn_ami_to_mapping_get.images_info_by_name(client, images_names, args.quiet)
        initial_images_map = cfn_ami_to_mapping_enrich.images_info_with_id(full_images_info, initial_images_map_with_image_name)
    images_map = cfn_ami_to_mapping_generate.cfn_ami_mapping_section(initial_images_map, aws_regions, args.map_name, args.quiet, args.aws_access_key_id, args.aws_secret_access_key)
    if args.json:
        print(Transform.dictionary_to_json(images_map))
    elif args.yaml:
        print(Transform.dictionary_to_yaml(images_map))

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt):
        print("[-] Processing has been stopped. Interrupted by user")
        exit(1)