import boto3
import os

stsclient = boto3.client('sts')

def assume_role(account_id,role_name):
    roleArn = "arn:aws:iam::{}:role/{}".format(account_id,role_name)
    assumed_role_object = stsclient.assume_role(
        RoleArn=roleArn,
        RoleSessionName="AssumeRoleSession1")

    credentials = assumed_role_object['Credentials']
    os.environ['AWS_ACCESS_KEY_ID'] = credentials['AccessKeyId']
    os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['SecretAccessKey']
    os.environ['AWS_SESSION_TOKEN'] = credentials['SessionToken']

    return os.environ['AWS_ACCESS_KEY_ID'],os.environ['AWS_SECRET_ACCESS_KEY'],os.environ['AWS_SESSION_TOKEN']


def unset_aws_environment_variables():
    os.environ.pop('AWS_ACCESS_KEY_ID',None)
    os.environ.pop('AWS_SECRET_ACCESS_KEY',None)
    os.environ.pop('AWS_SESSION_TOKEN',None)


assume_role('mgmt_account_id','customRoleForPython')

ram_client = boto3.client('ram',
                      aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                      aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                      aws_session_token=os.environ['AWS_SESSION_TOKEN']
                      )

response = ram_client.list_resources(resourceOwner='SELF')
print(response)

unset_aws_environment_variables()
assume_role('account_id','codebuildforpython')

ec2_client = boto3.client('ec2',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        aws_session_token=os.environ['AWS_SESSION_TOKEN']
                )

response = ec2_client.describe_vpcs()
print(response)


#print(response)
