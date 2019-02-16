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

if __name__ == "__main__":
    dynamodb = boto3.resource('dynamodb')
    create_cinema_table(dynamodb)
