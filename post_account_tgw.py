import boto3
ram_client = boto3.client('ram', region_name='your-region')
resource_share_arn = 'arn:aws:ram:your-region:your-account-id:resource-share/your-resource-share-id'
resource_share_details = ram_client.get_resource_share(resourceShareArn=resource_share_arn)
new_account_id = 'new-account-id'
resource_share_details['resourceShare']['principals'][0]['resourceShareArn'] = f'arn:aws:ram:your-region:{new_account_id}:resource-share/your-resource-share-id'
ram_client.update_resource_share(
    resourceShareArn=resource_share_arn,
    allowExternalPrincipals=True,
    resourceShareName='your-updated-resource-share-name',
    principals=[{'resourceShareArn': f'arn:aws:ram:your-region:{new_account_id}:resource-share/your-resource-share-id'}],
    version=resource_share_details['resourceShare']['version']
)


TGW Acceptance

import boto3

# Create EC2 client
ec2_client = boto3.client('ec2', region_name='your_region')

# Example Transit Gateway Attachment ID
attachment_id = ''

# Accept Transit Gateway Attachment
try:
    response = ec2_client.accept_transit_gateway_vpc_attachment(
        TransitGatewayAttachmentId=attachment_id
    )
    print("Transit Gateway Attachment accepted successfully:", response)
except Exception as e:
    print("Error accepting Transit Gateway Attachment:", str(e))

list of subnets of vpc

import boto3

# Create an EC2 client
ec2 = boto3.client('ec2')

# Retrieve all VPCs
response = ec2.describe_vpcs()
vpc_id = ""
for vpc in response['Vpcs']:
    vpc_id = vpc['VpcId']
    
vpc_id = vpc['VpcId']
subnet_ids = []

def list_subnets_of_vpc(vpc_id):
    # Retrieve subnets for the specified VPC
    response = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    subnets = response['Subnets']
    for subnet in subnets:
        subnet_ids.append(subnet['SubnetId'])
list_subnets_of_vpc(vpc_id)
print(subnet_ids)


TGW Attachment

import boto3

# Create EC2 and TGW clients
ec2_client = boto3.client('ec2', region_name='your_region')
tgw_client = boto3.client('ec2', region_name='your_region')

# Example Transit Gateway Attachment parameters
transit_gateway_id = ''


# Create Transit Gateway Attachment
try:
    response = ec2_client.create_transit_gateway_vpc_attachment(
        TransitGatewayId=transit_gateway_id,
        VpcId=vpc_id,
        SubnetIds=subnet_ids,
        TagSpecifications=[
            {
                'ResourceType': 'transit-gateway-attachment',
                'Tags': [
                    {'Key': 'Name', 'Value': 'YourAttachmentName'}
                ]
            },
        ]
    )
    print("Transit Gateway Attachment created successfully:", response)
except Exception as e:
    print("Error creating Transit Gateway Attachment:", str(e))

TGW Route propgation 

import boto3

# Create EC2 client
ec2_client = boto3.client('ec2', region_name='your_region')

# Example Transit Gateway ID and Route Table ID
transit_gateway_id = 'tgw-0123456789abcdef0'
route_table_id = 'tgw-rtb-0123456789abcdef0'

# Create Transit Gateway Route Table Propagation
try:
    response = ec2_client.create_transit_gateway_route_table_propagation(
        TransitGatewayRouteTableId=route_table_id,
        TransitGatewayAttachmentId='tgw-attach-0123456789abcdef0',
        TransitGatewayId=transit_gateway_id
    )
    print("Transit Gateway Route Table Propagation created successfully:", response)
except Exception as e:
    print("Error creating Transit Gateway Route Table Propagation:", str(e))


# Create Transit Gateway Attachment Association
    ec2_client.associate_transit_gateway_route_table(
        TransitGatewayAttachmentId=attachment_id,
        TransitGatewayRouteTableId='tgw-rtb-0123456789abcdef0'
    )

### List of shared invitation

 response = ram_client.get_resource_share_invitations()
        invitations = response.get('resourceShareInvitations', [])

        if invitations:
            print("Resource Share Invitations:")
            for invitation in invitations:
                invitation_id = invitation['resourceShareInvitationArn'].split('/')[-1]
                print(f"Invitation ID: {invitation_id}")
                print(f"Sender Account ID: {invitation['senderAccountId']}")
                print(f"Resource Share Name: {invitation['resourceShareName']}")
                print(f"Status: {invitation['status']}")
                print("\n---\n")

### Resource Invitation Acceptance

  response = ram_client.accept_resource_share_invitation(
            resourceShareInvitationArn=share_invitation_id
        )


Assume Role

import boto3

# Create an STS client
sts_client = boto3.client('sts')

# The ARN of the role you want to assume
role_to_assume_arn = 'arn:aws:iam::account-id-with-role:role/RoleName'

# The name you assign to the temporary credentials
role_session_name = 'YourSessionName'

# Assume the role
try:
    response = sts_client.assume_role(
        RoleArn=role_to_assume_arn,
        RoleSessionName=role_session_name
    )

    # Extract temporary credentials
    credentials = response['Credentials']

    print("Assumed role successfully. Temporary credentials:")
    print("Access Key:", credentials['AccessKeyId'])
    print("Secret Key:", credentials['SecretAccessKey'])
    print("Session Token:", credentials['SessionToken'])

except Exception as e:
    print("Error assuming role:", str(e))


Unset the variables

import os

# Unset AWS credentials
os.environ.pop('AWS_ACCESS_KEY_ID', None)
os.environ.pop('AWS_SECRET_ACCESS_KEY', None)
os.environ.pop('AWS_SESSION_TOKEN', None)

print("AWS credentials unset.")

aws ecs describe-tasks --cluster your-cluster-name --query 'tasks[].taskArn' --output json | jq -r '.[] | split("/") | last'

aws ecs list-tasks --cluster your-cluster-name --query 'taskArns' --output text

aws ecs stop-task --cluster your-cluster-name --task your-task-id

