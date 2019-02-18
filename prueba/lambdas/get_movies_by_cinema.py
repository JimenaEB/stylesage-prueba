import boto3

from boto3.dynamodb.conditions import Key, Attr

def get_movies_by_cinema(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')
    table = dynamodb.Table('cinemas')

    response = table.query(
        KeyConditionExpression=Key('cinema').eq(event.get('cinema'))
    )

    return {
        'statusCode': 200,
        'body': format_response(response)
    }

def format_response(response):
    return {'movies': response.get('Items')[0].get('movies'), 'count': len(response.get('Items')[0].get('movies'))}
