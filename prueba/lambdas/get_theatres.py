import boto3

def get_theatres(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')
    table = dynamodb.Table('theatres')

    response = table.scan(
        ProjectionExpression='theatre'
    )

    return {
        'statusCode': 200,
        'body': format_response(response)
    }

def format_response(response):
    list_theatres = []

    for theatre in response.get("Items"):
        list_theatres.append(theatre.get("theatre"))

    theatres = list(set(list_theatres))
    return {'theatre': theatres, 'count': len(theatres)}
