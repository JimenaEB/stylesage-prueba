import boto3

from scrapy.exceptions import DropItem

class DynamoDbPipeline(object):
    """Pipeline to store objects in dynamodb"""
    def process_item(self, item, spider):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(f'{spider.name}s')

        table.put_item(Item=item)

        return item
