import boto3
import sys
import json
import argparse

client = boto3.client('sso-admin')

## Identity Center arn
InstanceArn = ""

## Permission 
PermissionSetArn = "" 

parser = argparse.ArgumentParser(
            prog = 'permission set creation',
            description = ''
         )

parser.add_argument('-n','--permission_set_name',help="ex. ",required=True)
parser.add_argument('-d','--desc',help="Description such as project name for which permission set is being created like",required=True)
args = parser.parse_args()

aws_mgmt_polices = client.list_managed_policies_in_permission_set(
                InstanceArn= InstanceArn,
                PermissionSetArn= PermissionSetArn
                )

aws_managed_policies_arns = []

for aws_policy in aws_mgmt_polices['AttachedManagedPolicies']:
    aws_managed_policies_arns.append(aws_policy['Arn'])

create_permission_set = client.create_permission_set(
            Name = args.permission_set_name,
            Description = '{} Account Architect Role Permissionset'.format(args.desc),
            InstanceArn = InstanceArn,
             Tags = [
                    {
                     'Key': 'Policy',
                     'Value': 'ApplicationSpecific'
                     },
                ]
            )
permissionSetArn = create_permission_set['PermissionSet']['PermissionSetArn']

for policy_arn in aws_managed_policies_arns: 
    attach_managed_policies = client.attach_managed_policy_to_permission_set(
            InstanceArn = InstanceArn,
            PermissionSetArn = permissionSetArn,
            ManagedPolicyArn= policy_arn
        )
