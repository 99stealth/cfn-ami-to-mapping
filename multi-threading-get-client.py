from itertools import repeat
import time
import concurrent.futures
import boto3


start_time = time.time()


def get_client(region, resource='ec2'):
#    try:
#    time.sleep(random.uniform(0.1, 0.9))
    return boto3.client(resource, region_name=region)
#    except ClientError as e:
#        print('Unexpected error: {}'.format(e))
#    except ParamValidationError as e:
#        print('Parameter validation error: {}'.format(e))


def get_aws_regions():
    client = get_client('us-east-1')
    return [region['RegionName'] for region in client.describe_regions()['Regions']]


with concurrent.futures.ThreadPoolExecutor() as executor:
    regions = get_aws_regions()
    results = executor.map(get_client, regions, repeat('ec2'))

    clients = [r for r in results]

    client_per_region = dict(zip(regions, clients))
    print(client_per_region)

end_time = time.time()

print(end_time - start_time)
