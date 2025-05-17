import boto3
import sys
import json
import argparse

client = boto3.client('sso-admin')

parser = argparse.ArgumentParser(
                    prog = 'permission set creation',
                    description = 'permissionSet creation based on N16 Tek Developer'
                    )

parser.add_argument('-n','--permission-set-name',required=True)

args = parser.parse_args()

InstanceArn = ""
PermissionSetArn = ""

customer_managed_policies = {}

def customer_managed_policies():
    cs_mgmt_polices = client.list_customer_managed_policy_references_in_permission_set(
        InstanceArn= InstanceArn,
        PermissionSetArn= PermissionSetArn,
        MaxResults=20
        )
    customer_managed_policies_name = []
    customer_managed_policies_path = []
    for cp in cs_mgmt_polices['CustomerManagedPolicyReferences']:
        customer_managed_policies_name.append(cp['Name'])
        customer_managed_policies_path.append(cp['Path'])
    customer_managed_policies = dict(zip(customer_managed_policies_name, customer_managed_policies_path))

aws_managed_policies_arns = []

def aws_managed_policies():
    aws_mgmt_polices = client.list_managed_policies_in_permission_set(
                InstanceArn= InstanceArn,
                PermissionSetArn= PermissionSetArn
                )
    for aws_policy in aws_mgmt_polices['AttachedManagedPolicies']:
        aws_managed_policies_arns.append(aws_policy['Arn'])

def permission_set_create():
    create_permission_set = client.create_permission_set(
            Name = args.permission-set-name,
            Description = '{} Account Developer Role Permissionset'.format(args.permission-set-name),
            InstanceArn = InstanceArn
            )
    permissionSetArn = create_permission_set['PermissionSet']['PermissionSetArn']
    return permissionSetArn

permissionSetArn =  permission_set_create()

aws_managed_policies()
def attach_aws_managed_policy():
    for policy_arn in aws_managed_policies_arns:
        attach_managed_policies = client.attach_managed_policy_to_permission_set(
            InstanceArn = InstanceArn,
            PermissionSetArn = permissionSetArn,
            ManagedPolicyArn= policy_arn
        )

customer_managed_policies()
def attach_customer_policy():
    for Name,Path in customer_managed_policies.items():
        attach_customer_policies = client.attach_customer_managed_policy_reference_to_permission_set(
            InstanceArn= InstanceArn,
            PermissionSetArn= permissionSetArn,
            CustomerManagedPolicyReference={
                'Name': Name,
                'Path': Path
                }
            )

def attach_inline_policy():
    f = open('policy.json')
    f_json = json.load(f)
    f_str = json.dumps(f_json)

    inline_policy = client.put_inline_policy_to_permission_set(
        InstanceArn = InstanceArn,
        PermissionSetArn = permissionSetArn,
        InlinePolicy = f_str
        )
    f.close()

attach_inline_policy
