import boto3
import argparse

parser = argparse.ArgumentParser(description="Provide the information of account and permissionset to delete it.")
parser.add_argument('-a','--account_id', type=int, help="AWS Account ID", required=True)
parser.add_argument('-gname','--group_name', type=str, help="Group Name for permissionSet which we want to delete",required=True)
parser.add_argument('-n','--permission_set_name', type=str, help="Permission Set Name which we want to de-attach or remove from account",required=True)

# Parse arguments
args = parser.parse_args()


def get_permission_set_arn(permission_set_name, instance_arn):
    client = boto3.client('sso-admin')
    
    # List all permission sets
    permission_sets = client.list_permission_sets(InstanceArn=instance_arn)['PermissionSets']
    
    # Loop through permission sets to find the ARN of the specified permission set name
    for permission_set_arn in permission_sets:
        response = client.describe_permission_set(
            InstanceArn=instance_arn,
            PermissionSetArn=permission_set_arn
        )
        
        # Check if the permission set name matches
        if response['PermissionSet']['Name'] == permission_set_name:
            return permission_set_arn
    
    return None


def get_group_id(group_name, instance_arn):
    # List all groups in the SSO instance
    response = client.list_groups(InstanceArn=instance_arn)
    
    # Search for the group with the specified name
    for group in response['Groups']:
        if group['DisplayName'] == group_name:
            return group['GroupId']
    
    return None


def delete_account_assignments(instance_arn, permission_set_arn, principal_type, principal_id, account_ids):
    for account_id in account_ids:
        try:
            response = client.delete_account_assignment(
                InstanceArn=instance_arn,
                TargetId=account_id,
                TargetType='AWS_ACCOUNT',
                PermissionSetArn=permission_set_arn,
                PrincipalType=principal_type,
                PrincipalId=principal_id
            )
            
            # Check the status of deletion
            status = response.get('AccountAssignmentDeletionStatus', {}).get('Status')
            print(f"Deletion status for Account ID {account_id}: {status}")
        
        except client.exceptions.ResourceNotFoundException:
            print(f"Account assignment not found for Account ID {account_id}")
        except client.exceptions.ConflictException:
            print(f"Conflict encountered for Account ID {account_id}. It might already be deleted.")
        except Exception as e:
            print(f"An error occurred while deleting account assignment for Account ID {account_id}: {e}")


# Example usage
instance_arn = 'arn:aws:sso:::instance/ssoins-xxxxxxxxxxxx'  # Replace with your AWS SSO instance ARN
permission_set_name = args.permission_set_name  # Replace with the name of your permission set
permission_set_arn = get_permission_set_arn(permission_set_name, instance_arn)

group_name = args.group_name  # Replace with the name of your group
principal_type = 'GROUP'  # Or 'USER'
principal_id = get_group_id(group_name, instance_arn)  # Replace with the actual principal ID for the group or user
#account_ids = ['123456789012', '987654321098']  # Replace with a list of your account IDs
account_ids = args.account_id

delete_account_assignments(instance_arn, permission_set_arn, principal_type, principal_id, account_ids)

