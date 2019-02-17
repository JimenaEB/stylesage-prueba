import boto3

def create_cinema_table(dynamodb):
    """Create cinema table in dynamodb"""
    table = dynamodb.create_table(
        TableName='cinemas',
        KeySchema=[
            {
                'AttributeName': 'cinema',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'cinema',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='cinemas')

    if table.item_count == 0:
        print("Tabla cinemas creada con éxito")

def create_theatre_table(dynamodb):
    """Create theatre table in dynamodb"""
    table = dynamodb.create_table(
        TableName='theatres',
        KeySchema=[
            {
                'AttributeName': 'play_name',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'theatre',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'play_name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'theatre',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 3
        }
    )

if __name__ == "__main__":
    dynamodb = boto3.resource('dynamodb')
    try:
        create_cinema_table(dynamodb)
    except:
        print("Cinema table already exists")

    try:
        create_theatre_table(dynamodb)
    except:
        print("Theatre table already exists")
