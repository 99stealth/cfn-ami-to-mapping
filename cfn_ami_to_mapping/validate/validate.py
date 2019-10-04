import re


class Validate:
    def images_ids(self, images_ids):
        ''' The method receives the string with AMI ID and checks if it is
        valid. If everything is in order it will return True as a first
        argument and None as a second. Otherwise, if AMI ID is an invalid
        method will return False as a first argument and AMI ID as a second '''

        for image_id in images_ids:
            image_is_valid = re.match('^ami-(([a-f0-9]{8}$)|([a-f0-9]{17}$))', image_id)
            if not image_is_valid:
                return False, image_id
        return True, None

    def aws_access_key_id(self, aws_access_key_id):
        ''' The method receives the string with AWS Access Key ID and checks if
        it is valid. If everything is in order it will return True otherwise
        it returns False '''

        if re.match('^AK[A-Z0-9]{18}$', aws_access_key_id):
            return True
        else:
            return False

    def aws_secret_access_key(self, aws_secret_access_key):
        ''' The method receives the string with AWS Secret Access Key and
        checks if it is valid. If everything is in order it will return True
        otherwise it returns False '''

        if re.match('^[A-Za-z0-9+=/]{40}$', aws_secret_access_key):
            return True
        else:
            return False

    def aws_regions(self, aws_regions, regions_provided_by_user):
        for provided_region in regions_provided_by_user:
            if provided_region not in aws_regions:
                return False, provided_region
        return True, None
