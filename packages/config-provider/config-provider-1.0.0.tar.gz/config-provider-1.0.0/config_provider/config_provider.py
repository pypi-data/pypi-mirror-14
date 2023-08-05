"""
Look up sensitive configuration items such as credentials and keys
so they don't need to be hardcoded as artifacts in the code repository.
This implementation finds it's resources in the DynamoDB table called 'config_provider'
"""

import boto
import boto.dynamodb
import json
from collections import defaultdict


class ConfigProvider(object):

    _ENVIRONMENT_DEFAULT_NAME = 'default_config'
    _DYNAMO_DB_TABLE = 'config_provider'

    def __init__(self, environment_name):

        # Front load all resources early to fail fast if there is a retrieval or parsing problem
        self._resources = defaultdict(dict)
        self._load_resources_from_dynamo_db(self._ENVIRONMENT_DEFAULT_NAME)
        self._load_resources_from_dynamo_db(environment_name.lower() + "_config")

    def __getitem__(self, resource_name):
        return self._resources[resource_name]

    def _load_resources_from_dynamo_db(self, environment_name):
        conn = boto.dynamodb.connect_to_region(region_name="us-east-1")
        table = conn.get_table(self._DYNAMO_DB_TABLE)
        result_set = table.scan()
        for key in [row["component"] for row in result_set]:
            item = table.get_item(hash_key=key)
            try:
                config = item.get(environment_name)
                if config:
                    resource_dict = json.loads(config)
                    self._resources[key].update(resource_dict)
            except Exception as e:
                raise Exception('Problem decoding json in {0}. Reason: {1}'.format(key, e.message))
