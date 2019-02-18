import boto3

def get_cinemas(event, context):
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-3')
    table = dynamodb.Table('cinemas')

    response = table.scan(
        ProjectionExpression='cinema'
    )

    return {
        'statusCode': 200,
        'body': format_response(response)
    }

def format_response(response):
    list_cinemas = []

    for cinema in response.get("Items"):
        list_cinemas.append(cinema.get("cinema"))

    return {'cinemas': list_cinemas, 'count': response.get("Count")}
