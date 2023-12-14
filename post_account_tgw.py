import boto3
import os

stsclient = boto3.client('sts')

assumed_role_object = stsclient.assume_role(
    RoleArn="<arn>",
    RoleSessionName="AssumeRoleSession1")

credentials = assumed_role_object['Credentials']

ram_client = boto3.client('ram',
                      aws_access_key_id=credentials['AccessKeyId'],
                      aws_secret_access_key=credentials['SecretAccessKey'],
                      aws_session_token=credentials['SessionToken'],
                      )


response = ram_client.associate_resource_share(
    resourceShareArn='<RAM_ARN>',
    resourceArns=['<TransitGateway_ARN'],
    principals=['AccountID'],
)

print(response)

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


#TGW Attachment ID

import boto3

# Create an EC2 client
ec2_client = boto3.client('ec2')

# Specify the Transit Gateway ID
transit_gateway_id = 'your-transit-gateway-id'

# Describe Transit Gateway attachments
response = ec2_client.describe_transit_gateway_attachments(
    Filters=[
        {
            'Name': 'transit-gateway-id',
            'Values': [transit_gateway_id]
        },
    ]
)

# Extract and print Transit Gateway attachment IDs
for attachment in response['TransitGatewayAttachments']:
    attachment_id = attachment['TransitGatewayAttachmentId']
    print(f"Transit Gateway Attachment ID: {attachment_id}")


### TGW create route association

import boto3

# Specify the Transit Gateway ID
transit_gateway_id = 'your_transit_gateway_id'

# get transit gateway id
response = ec2.describe_transit_gateway_route_tables(TransitGatewayId=transit_gateway_id)

route_table_id = response['TransitGatewayRouteTables'][0]['TransitGatewayRouteTableId']
print(f"Transit Gateway Route Table ID: {route_table_id}")

# Specify the attachment ID to associate with the route table
attachment_id = 'your_attachment_id'

# Associate the route table with the attachment
ec2_client.associate_transit_gateway_route_table(
    TransitGatewayRouteTableId=route_table_id,
    TransitGatewayAttachmentId=attachment_id
)

print(f"Route table {route_table_id} created and associated with attachment {attachment_id}")




### Enable TGW Route Attachment Propagation

import boto3

# Create a Boto3 Transit Gateway client
client = boto3.client('ec2', region_name='your_region')

# Specify the Transit Gateway ID
transit_gateway_id = 'your_transit_gateway_id'

# Specify the attachment IDs (resource IDs of VPCs, VPNs, etc.)
attachment_ids = ['attachment_id_1', 'attachment_id_2']

# Enable route propagation for the specified attachments
for attachment_id in attachment_ids:
    response = client.enable_transit_gateway_route_table_propagation(
        TransitGatewayRouteTableId='your_route_table_id',
        TransitGatewayAttachmentId=attachment_id
    )
    print(f"Enabled route propagation for attachment {attachment_id}")

# Disable route propagation for the specified attachments
for attachment_id in attachment_ids:
    response = client.disable_transit_gateway_route_table_propagation(
        TransitGatewayRouteTableId='your_route_table_id',
        TransitGatewayAttachmentId=attachment_id
    )
    print(f"Disabled route propagation for attachment {attachment_id}")



# Create Transit Gateway Attachment Association
    ec2_client.associate_transit_gateway_route_table(
        TransitGatewayAttachmentId=attachment_id,
        TransitGatewayRouteTableId='<>'
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


Get of list of resource in RAM

import boto3

# Replace 'your-region' with your actual AWS region
region = 'your-region'

# Create a Boto3 RAM client
ram_client = boto3.client('ram', region_name=region)

# Get the list of resources shared with the current account
response_resources = ram_client.get_resource_shares(
    resourceOwner='SELF'
)

# Extract resource information
shared_resources = response_resources.get('resources', [])
for resource in shared_resources:
    resource_name = resource.get('name', 'N/A')
    resource_type = resource.get('resourceType', 'N/A')
    resource_arn = resource.get('resourceArn', 'N/A')
    
    print(f"Resource Name: {resource_name}, Resource Type: {resource_type}, Resource ARN: {resource_arn}")

# Get the list of principals (accounts) that the current account has shared resources with
response_principals = ram_client.get_resource_share_associations(
    associationType='PRINCIPAL',
    resourceOwner='SELF'
)

# Extract principal information
shared_principals = response_principals.get('resourceShareAssociations', [])
for principal in shared_principals:
    principal_account_id = principal.get('associatedEntity', {}).get('id', 'N/A')
    principal_type = principal.get('associatedEntity', {}).get('type', 'N/A')
    
    print(f"Principal Account ID: {principal_account_id}, Principal Type: {principal_type}")


IAM crossAccount

# iam.tf

resource "aws_iam_role" "cross_account_role" {
  name = "cross-account-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        AWS = "arn:aws:iam::ACCOUNT_B_ID:root"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "cross_account_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess" # or any other policy
  role       = aws_iam_role.cross_account_role.name
}
