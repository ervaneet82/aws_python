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


TGW Attachment

import boto3

# Create EC2 and TGW clients
ec2_client = boto3.client('ec2', region_name='your_region')
tgw_client = boto3.client('ec2', region_name='your_region')

# Example Transit Gateway Attachment parameters
transit_gateway_id = ''
vpc_id = ''
subnet_id = ''

# Create Transit Gateway Attachment
try:
    response = ec2_client.create_transit_gateway_vpc_attachment(
        TransitGatewayId=transit_gateway_id,
        VpcId=vpc_id,
        SubnetIds=[subnet_id],
        TagSpecifications=[
            {
                'ResourceType': 'transit-gateway-attachment',
                'Tags': [
                    {'Key': 'Name', 'Value': 'YourAttachmentName'}
                    # Add more tags as needed
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

