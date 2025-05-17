import boto3
import os

stsclient = boto3.client('sts')

assumed_role_object = stsclient.assume_role(
    RoleArn="arn:aws:iam::141803583963:role/customRoleForPython",
    RoleSessionName="AssumeRoleSession1")

credentials = assumed_role_object['Credentials']

identityStore = boto3.client('identitystore',
                      aws_access_key_id=credentials['AccessKeyId'],
                      aws_secret_access_key=credentials['SecretAccessKey'],
                      aws_session_token=credentials['SessionToken'],
                      )
