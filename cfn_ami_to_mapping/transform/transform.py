import json
import yaml


class Transform:
    def dictionary_to_json(self, images_map):
        ''' Function receives images map and transforms it ro json '''
        return json.dumps(images_map, indent=4, sort_keys=True)

    def dictionary_to_yaml(self, images_map):
        ''' Function receives images map and transforms it ro yaml '''
        return yaml.dump(images_map)
