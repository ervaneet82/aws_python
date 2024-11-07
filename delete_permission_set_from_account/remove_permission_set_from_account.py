import boto3

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

# Example usage
instance_arn = 'arn:aws:sso:::instance/ssoins-xxxxxxxxxxxx'  # Replace with your AWS SSO instance ARN
permission_set_name = 'YourPermissionSetName'  # Replace with the name of your permission set
permission_set_arn = get_permission_set_arn(permission_set_name, instance_arn)


def get_group_id(group_name, instance_arn):
    # List all groups in the SSO instance
    response = client.list_groups(InstanceArn=instance_arn)
    
    # Search for the group with the specified name
    for group in response['Groups']:
        if group['DisplayName'] == group_name:
            return group['GroupId']
    
    return None

# Example usage
instance_arn = 'arn:aws:sso:::instance/ssoins-xxxxxxxxxxxx'  # Replace with your AWS SSO instance ARN
group_name = 'YourGroupName'  # Replace with the name of your group
group_id = get_group_id(group_name, instance_arn)

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
permission_set_arn = 'arn:aws:sso:::permissionSet/ssoins-xxxxxxxxxxxx/ps-xxxxxxxxxxxx'  # Replace with your Permission Set ARN
principal_type = 'GROUP'  # Or 'USER'
principal_id = 'your-principal-id'  # Replace with the actual principal ID for the group or user
account_ids = ['123456789012', '987654321098']  # Replace with a list of your account IDs

delete_account_assignments(instance_arn, permission_set_arn, principal_type, principal_id, account_ids)

