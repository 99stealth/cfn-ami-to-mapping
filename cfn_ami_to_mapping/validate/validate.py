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