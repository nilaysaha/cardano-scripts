#~/bin/env python3

"""
This module is supposed to store the incoming minting request in dynamoDB so that we can then build services for people who are using the platform 
to retrieve their information and later provide services to them based on that. Also we can know what the final footprint of a particular minting
request is, which mostly would be lost otherwise.
Reference:https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
"""

import boto3

class StoreEvent:
    def __init__(self, name, table):
        self.dbname = name
        self.db = boto3.resource('dynamodb')
        self.table = self.db.Table(tablename)

    def create_item(self, item):
        t = self.table.put_item(Item=item)
        return t

    def get_item(self, key):
        """
        sample key: Just an example
        {
        'user_uuid': 'ad2e77f4-e05a-4458-8a18-a7fe1d56fea8',
        'last_name': 'Doe'
        }
        """
        response = self.table.get_item(key)
        item = response['Item']
        print(item)
        return item
