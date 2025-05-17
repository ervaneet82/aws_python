import boto3
import os
import sys
import ram_resource
from ram_resource import target_account_id
from ram_resource import assume_role
from ram_resource import mgmt_account_id
from ram_resource import mgmt_role_name
from ram_resource import unset_aws_environment_variables


stsclient = boto3.client('sts')

transit_gateway_id = ''

assume_role(mgmt_account_id,mgmt_role_name)

ram_client = boto3.client('ram',
                          AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID'],
                          AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY'],
                          AWS_SESSION_TOKEN = os.environ['AWS_SESSION_TOKEN']
                          )

def ram_tgw_share_to_target_account(account_id_to_share):
    response = ram_client.associate_resource_share(
        resourceShareArn="<>",
        resourceArns=["<tgw-resource_arn>"],
        principals=[account_id_to_share]
    )

ram_tgw_share_to_target_account(target_account_id) # Target Acccount

unset_aws_environment_variables()

assume_role(target_account_id,'my_aft_role')

def ram_share_acceptance_target_account():
    print("Accepting RAM share for TGW...")
    ram_client = boto3.client('ram',
                              AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID'],
                              AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY'],
                              AWS_SESSION_TOKEN = os.environ['AWS_SESSION_TOKEN']
                          )
    response = ram_client.get_resource_share_invitations()
    for invite in response['resourceShareInvitations']:
        resourcesharearn = invite['resourceShareInvitationArn']
    ram_acceptance = ram_client.accept_resource_share_invitation(
        resourceShareInvitationArn = resourcesharearn
    )
    print(ram_acceptance)

ram_share_acceptance_target_account()

def list_subnets_of_vpc():
    vpc_id = ""
    subnet_ids = []
    ec2 = boto3.resource('ec2',
                         AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID'],
                         AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY'],
                         AWS_SESSION_TOKEN = os.environ['AWS_SESSION_TOKEN']
                         )
    response = ec2.describe_vpcs()
    for vpc in response['Vpcs']:
        vpc_id = vpc['VpcId']

    vpc_id = vpc['VpcId']
    response = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    subnets = response['Subnets']
    for subnet in subnets:
        subnet_ids.append(subnet['SubnetId'])
    return subnet_ids,vpc_id

subnet_ids,vpc_id = list_subnets_of_vpc()
print(subnet_ids)

def create_transit_gateway_attachment():
    try:
        ec2 = boto3.client('ec2',
                            AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID'],
                            AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY'],
                            AWS_SESSION_TOKEN = os.environ['AWS_SESSION_TOKEN']
                           )
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

    route_tables = ec2.describe_route_tables(Filters=[{'Name': 'vpc-id','Values':[vpc_id]}])
    route_table_id = ""

    for route_table in route_tables['RouteTables']:
        route_table_id = route_table['RouteTableId']

    route_table_entry = ec2.create_route(
        RouteTableId=route_table_id,
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=transit_gateway_id
    )

    print(route_table_entry)

    response = ec2.describe_transit_gateway_attachments(
        Filters=[
            {
                'Name': 'transit-gateway-id',
                'Values': [transit_gateway_id]
            },
            {
                'Name': 'vpc-id',
                'Values': [vpc_id]
            }
        ]
    )

    # Extract and print Transit Gateway Attachment IDs
    for attachment in response['TransitGatewayAttachments']:
        if attachment['State'] == 'available':
            attachment_id = attachment['TransitGatewayAttachmentId']
            print(f"Transit Gateway Attachment ID: {attachment_id}")

    return attachment_id

TransitGatewayAttachment_Id = create_transit_gateway_attachment()

unset_aws_environment_variables()

assume_role(mgmt_account_id,mgmt_role_name) # Management Account

def mgmt_tgw_rt_association():
    ec2 = boto3.client('ec2',
                       AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID'],
                       AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY'],
                       AWS_SESSION_TOKEN = os.environ['AWS_SESSION_TOKEN']
                       )

    response = ec2.describe_transit_gateway_route_tables()

    route_table_id = response['TransitGatewayRouteTables'][0]['TransitGatewayRouteTableId']

    ec2.associate_transit_gateway_route_table(
        TransitGatewayAttachmentId = TransitGatewayAttachment_Id,
        TransitGatewayRouteTableId = route_table_id
    )

    ec2.disable_transit_gateway_route_table_propagation(
        TransitGatewayAttachmentId = TransitGatewayAttachment_Id,
        TransitGatewayRouteTableId = route_table_id
    )

mgmt_tgw_rt_association()
