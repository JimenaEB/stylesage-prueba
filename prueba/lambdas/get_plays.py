import boto3

def get_plays(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')
    table = dynamodb.Table('theatres')

    response = table.scan()

    return {
        'statusCode': 200,
        'body': {'plays': response.get("Items"), 'count': response.get("Count")}
    }
