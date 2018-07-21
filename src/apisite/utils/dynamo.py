import boto3

USER_TABLE_NAME = "User"
PEOPLE_TABLE_NAME = "People"
DEFAULT_PEOPLE_TYPE = 1

def connect_dynamo(aki, sak, region):
    return boto3.client("dynamodb", aws_access_key_id = aki,
        aws_secret_access_key=sak, region_name=region)

def create_people_table(client):
    kwargs = {}
    kwargs["AttributeDefinitions"] = [
    {
        'AttributeName': 'PeopleType',
        'AttributeType': 'N'
    },
    {
        'AttributeName': 'NameWorkPlace',
        'AttributeType': 'S'
    }
    ]
    kwargs["TableName"] = PEOPLE_TABLE_NAME
    kwargs["KeySchema"] = [
    {
        'AttributeName': 'PeopleType',
        'KeyType': 'HASH'
    },
    {
        'AttributeName': 'NameWorkPlace',
        'KeyType': 'RANGE'
    }
    ]
    kwargs["ProvisionedThroughput"] = {
        'ReadCapacityUnits': 1000,
        'WriteCapacityUnits': 100,
    }
    resp = client.create_table(**kwargs)

def put_people(client, people_id, name, workplace, position):
    items = {}
    items["PeopleType"] = DEFAULT_PEOPLE_TYPE
    items["NameWorkPlace"] = "%s,%s" % (name, workplace)
    items["PeopleId"] = people_id
    items["Position"] = position

    kwargs = {}
    kwargs["TableName"] = PEOPLE_TABLE_NAME
    kwargs["Item"] = items
    kwargs["ReturnConsumedCapacity"] = 'NONE'

    client.put_item(**kwargs)

def query_peple(client, prefix, limit=10):
    kwargs = {}
    kwargs["TableName"] = PEOPLE_TABLE_NAME
    kwargs["ConsistentRead"] = False
    kwargs["Select"] = 'SPECIFIC_ATTRIBUTES'
    kwargs["AttributesToGet"] = ["NameWorkPlace", "PeopleId", "Position"]
    kwargs["Limit"] = limit
    kwargs["ReturnConsumedCapacity"] = 'NONE'
    kwargs["KeyConditionExpression"] = "PeopleType = :people_type AND begins_with ( NameWorkPlace, :prefix )"
    kwargs["ExpressionAttributeValues"] = {":people_type": {"N": str(DEFAULT_PEOPLE_TYPE)},
                                           ":prefix": {"S": prefix}}
    resp = client.query(**kwargs)
    items = []
    if resp.has_key('Items'):
        items = resp["Items"]
    for x in items:
        yield x["NameWorkPlace"], x["PeopleId"], x["Position"]


def create_user_table(client):
    kwargs = {}
    kwargs["AttributeDefinitions"] = [
    {
        'AttributeName': 'UserName',
        'AttributeType': 'S'
    }
    ]
    kwargs["TableName"] = USER_TABLE_NAME
    kwargs["KeySchema"] = [
    {
        'AttributeName': 'UserName',
        'KeyType': 'HASH'
    }
    ]
    kwargs["ProvisionedThroughput"] = {
        'ReadCapacityUnits': 100,
        'WriteCapacityUnits': 10,
    }
    resp = client.create_table(**kwargs)

def get_user(client, username):
    kwargs = {}
    kwargs["TableName"] = USER_TABLE_NAME
    kwargs["Key"] = {'UserName': {'S': username}}
    kwargs["ConsistentRead"] = True
    response = client.get_item(**kwargs)
    if resp.has_key['Item']:
        return (resp['Item']['Password'], int(resp['Item']['PeopleId']))
    else:
        return None

def put_user(client, username, password, people_id, overwrite=False):
    if not overwrite and get_user(client, username):
        raise DuplicateResources("%s user already exists" % username)

    items = {}
    items["UserName"] = {'S': username}
    items["Password"] = {'S': password}
    items["PeopleId"] = {'N': str(people_id)}

    kwargs = {}
    kwargs["TableName"] = USER_TABLE_NAME
    kwargs["Item"] = items
    kwargs["ReturnConsumedCapacity"] = 'NONE'

    client.put_item(**kwargs)

    for i in range(5):
        if get_user(client, username):
            return (password, people_id)

    return None
