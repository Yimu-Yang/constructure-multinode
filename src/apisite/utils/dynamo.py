# import boto3

# PEOPLE_TABLE_NAME = "People"
# COMPANY_TABLE_NAME = "Company"
# DEFAULT_PEOPLE_TYPE = 1
# DEFAULT_COMPANY_TYPE = 1

# def connect_dynamo(aki, sak, region):
#     return boto3.client("dynamodb", aws_access_key_id = aki,
#         aws_secret_access_key=sak, region_name=region)

# def create_people_table(client):
#     kwargs = {}
#     kwargs["AttributeDefinitions"] = [
#     {
#         'AttributeName': 'PeopleType',
#         'AttributeType': 'N'
#     },
#     {
#         'AttributeName': 'NameWorkPlace',
#         'AttributeType': 'S'
#     }
#     ]
#     kwargs["TableName"] = PEOPLE_TABLE_NAME
#     kwargs["KeySchema"] = [
#     {
#         'AttributeName': 'PeopleType',
#         'KeyType': 'HASH'
#     },
#     {
#         'AttributeName': 'NameWorkPlace',
#         'KeyType': 'RANGE'
#     }
#     ]
#     kwargs["ProvisionedThroughput"] = {
#         'ReadCapacityUnits': 1000,
#         'WriteCapacityUnits': 100,
#     }
#     resp = client.create_table(**kwargs)

# def put_people(client, people_id, name, workplace):
#     items = {}
#     items["PeopleType"] = DEFAULT_PEOPLE_TYPE
#     items["NameWorkPlace"] = "%s,%s" % (name, workplace)
#     items["PeopleId"] = people_id

#     kwargs = {}
#     kwargs["TableName"] = PEOPLE_TABLE_NAME
#     kwargs["Item"] = items
#     kwargs["ReturnConsumedCapacity"] = 'NONE'

#     client.put_item(**kwargs)

# def query_peple(client, prefix, limit=10):
#     kwargs = {}
#     kwargs["TableName"] = PEOPLE_TABLE_NAME
#     kwargs["ConsistentRead"] = False
#     kwargs["Select"] = 'SPECIFIC_ATTRIBUTES'
#     kwargs["AttributesToGet"] = ["NameWorkPlace", "PeopleId"]
#     kwargs["Limit"] = limit
#     kwargs["ReturnConsumedCapacity"] = 'NONE'
#     kwargs["KeyConditionExpression"] = "PeopleType = :people_type AND begins_with ( NameWorkPlace, :prefix )"
#     kwargs["ExpressionAttributeValues"] = {":people_type": {"N": str(DEFAULT_PEOPLE_TYPE)},
#                                            ":prefix": {"S": prefix}}
#     resp = client.query(**kwargs)
#     items = []
#     if resp.has_key('Items'):
#         items = resp["Items"]
#     for x in items:
#         yield x["NameWorkPlace"], x["PeopleId"]

# def create_company_table(client):
#     kwargs = {}
#     kwargs["AttributeDefinitions"] = [
#     {
#         'AttributeName': 'CompanyType',
#         'AttributeType': 'N'
#     },
#     {
#         'AttributeName': 'CompanyName',
#         'AttributeType': 'S'
#     }
#     ]
#     kwargs["TableName"] = COMPANY_TABLE_NAME
#     kwargs["KeySchema"] = [
#     {
#         'AttributeName': 'CompanyType',
#         'KeyType': 'HASH'
#     },
#     {
#         'AttributeName': 'CompanyName',
#         'KeyType': 'RANGE'
#     }
#     ]
#     kwargs["ProvisionedThroughput"] = {
#         'ReadCapacityUnits': 1000,
#         'WriteCapacityUnits': 100,
#     }
#     resp = client.create_table(**kwargs)

# def put_company(client, company_id, name):
#     items = {}
#     items["CompanyType"] = DEFAULT_COMPANY_TYPE
#     items["CompanyName"] = name
#     items["CompanyId"] = company_id

#     kwargs = {}
#     kwargs["TableName"] = COMPANY_TABLE_NAME
#     kwargs["Item"] = items
#     kwargs["ReturnConsumedCapacity"] = 'NONE'

#     client.put_item(**kwargs)

# def query_company(client, prefix, limit=10):
#     kwargs = {}
#     kwargs["TableName"] = COMPANY_TABLE_NAME
#     kwargs["ConsistentRead"] = False
#     kwargs["Select"] = 'SPECIFIC_ATTRIBUTES'
#     kwargs["AttributesToGet"] = ["CompanyName", "CompanyId"]
#     kwargs["Limit"] = limit
#     kwargs["ReturnConsumedCapacity"] = 'NONE'
#     kwargs["KeyConditionExpression"] = "CompanyType = :company_type AND begins_with ( CompanyName, :prefix )"
#     kwargs["ExpressionAttributeValues"] = {":company_type": {"N": str(DEFAULT_COMPANY_TYPE)},
#                                            ":prefix": {"S": prefix}}
#     resp = client.query(**kwargs)
#     items = []
#     if resp.has_key('Items'):
#         items = resp["Items"]
#     for x in items:
#         yield x["CompanyName"], x["CompanyId"]

