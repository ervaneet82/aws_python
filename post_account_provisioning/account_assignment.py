import boto3
import argparse
import sys

parser = argparse.ArgumentParser(
                    prog = 'permission set assigned to group and account',
                    description = 'permissionSet creation based on N16'
                    )

parser.add_argument('-g','--group_name',help='Group Name ',required=True)
parser.add_argument('-n','--permission_set_name',help='Permission Set Name which will associcate with Group ex. UICOE-Developer',required=True)
parser.add_argument('-e','--account_email_id',help='Provide the email id of account which has been created',required=True)

args = parser.parse_args()

IdentityStoreId = ''
InstanceArn = ''

client = boto3.client('identitystore')
org = boto3.client('organizations')
sso = boto3.client('sso-admin')

response = client.list_groups(
        IdentityStoreId = IdentityStoreId
        )

groupId = ""

for group in response['Groups']:
    if group['DisplayName'] == args.group_name:
        groupId = group['GroupId']

print("Group Id: ",groupId)

list_accounts = org.list_accounts()

paginator = org.get_paginator('list_accounts')
page_iterator = paginator.paginate()

accountId=""

for page in page_iterator:
    for acct in page['Accounts']:
        if acct['Email'] == args.account_email_id:
            accountId = acct['Id']

print("AccountId : ",accountId)
permission_sets = []

paginator = sso.get_paginator('list_permission_sets')
page_iterator = paginator.paginate(InstanceArn='')
for page in page_iterator:
    for permission_set in page['PermissionSets']:
        permission_sets.append(permission_set)

permission_set_arn = ""

for permission in permission_sets:
    describe_permission = sso.describe_permission_set(
            InstanceArn=InstanceArn,
            PermissionSetArn=permission
            )
    if describe_permission['PermissionSet']['Name'] == args.permission_set_name:
        permission_set_arn = describe_permission['PermissionSet']['PermissionSetArn']

print("PerimissionSet : ",permission_set_arn)


acct_group_perm_assignment = sso.create_account_assignment(
            InstanceArn=InstanceArn,
            TargetId=accountId,
            TargetType='AWS_ACCOUNT',
            PermissionSetArn=permission_set_arn,
            PrincipalType='GROUP',
            PrincipalId=groupId
        )

print(acct_group_perm_assignment)
