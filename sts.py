import boto3
stsclient = boto3.client('sts')

assumed_role_object = stsclient.assume_role(
        RoleArn="<>",
        RoleSessionName="AssumeRoleSession1")

credentials=assumed_role_object['Credentials']
print(credentials['AccessKeyId'],
      credentials['SecretAccessKey'],
      credentials['SessionToken']
      )
