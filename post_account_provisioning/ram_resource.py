import boto3
import os
import sys


s3 = boto3.client('s3')
ssm_client = boto3.client('ssm')

parameter_name = "/aft/account/ct-management/account-id"  # Replace with the actual parameter path


ssm_response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
mgmt_account_id = ssm_response['Parameter']['Value']
mgmt_role_name = 'customRoleForPython'

bucket_name = 'aft-account-provisioning-state'
object_key = 'account_id.txt'
local_file_path = 'account_id.txt'


try:
    s3.download_file(bucket_name,object_key,local_file_path)
    print(f"File downloaded successfully: {local_file_path}")
except Exception as e:
    print(f"Error downloaded file: {e}")

with open(local_file_path,'r'):
    accountID = file.read()

target_account_id = accountID.strip()

stsclient = boto3.client('sts')

transit_gateway_id = ''

def assume_role(account_id, role_name):
    roleArn = "arn:aws:iam::{}:role/{}".format(account_id,role_name)
    print("Role ARN : ",roleArn)
    assume_role_object= stsclient.assume_role(
        RoleArn=roleArn,
        RoleSessionName="AssumeSession1")
    credentials = assume_role_object['Credentials']
    os.environ['AWS_ACCESS_KEY_ID'] = credentials['AccessKeyId']
    os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['SecretAccessKey']
    os.environ['AWS_SESSION_TOKEN'] = credentials['SessionToken']
    return os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'],os.environ['AWS_SESSION_TOKEN']

def unset_aws_environment_variables():
    os.environ.pop('AWS_ACCESS_KEY_ID',None)
    os.environ.pop('AWS_SECRET_ACCESS_KEY',None)
    os.environ.pop('AWS_SESSION_TOKEN',None)
    print("AWS credentials unset.")

assume_role(mgmt_account_id,mgmt_role_name)
ram_client = boto3.client('ram',
                          AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID'],
                          AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY'],
                          AWS_SESSION_TOKEN = os.environ['AWS_SESSION_TOKEN']
                          )

# Get the list of resources shared with current account

response_resources = ram_client.get_resource_shares(
    resourceOwner='SELF',
    resourceShareArns = []
)
#Extract resource information
shared_resources = response_resources.get('resources',[])
for resource in shared_resources:
    resource_name = resource.get('name','N/A')
    resource_type = resource.get('resourceType','N/A')
    resource_arn = resource.get('resourceArn','N/A')
    print(f"Resource Name: {resource_name}, Resource Type: {resource_type}, Resource ARN: {resource_arn}")

# Get the list of principals (accounts) that the current account has shared resources
response_principals = ram_client.get_resource_share_associations(
    associationType='PRINCIPAL'
)

associated_principals = []

#Extract principal information
shared_principals = response_principals.get('resourceShareAssociations',[])
for principal in shared_principals:
    associated_principals.append(principal['associatedEntity'])

if target_account_id in associated_principals:
    print("{} Already exists in Resource Access Manager".format(target_account_id))
    sys.exit(0)
