import boto3

client = boto3.client('ec2')


regions = client.describe_regions()
list_regions = []

for region in regions['Regions']:
    list_regions.append(region['RegionName'])

for region in list_regions:
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.describe_vpcs(
        Filters=[
            {
                'Name': 'isDefault',
                'Values': ['true']
            },
        ]
    )
    try:
        vpcId = response['Vpcs'][0]['VpcId']
        subnets = ec2.describe_subnets(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [vpcId]
                }
            ]
        )

        for subnet in subnets['Subnets']:
            print("Deleting subnet in vpc {} region {} :".format(vpcId, region), subnet['SubnetId'])
            ec2.delete_subnet(SubnetId=subnet['SubnetId'])

        igws = ec2.describe_internet_gateways(
            Filters=[{
                'Name': 'attachment.vpc-id',
                'Values': [vpcId]
            }]
        )
        for igw in igws['InternetGateways']:
            print("Deleting internet gateway in vpc {} {} :".format(vpcId, region), igw['InternetGatewayId'])
            client.delete_internet_gateway(
                InternetGatewayId=igw['InternetGatewayId'],
            )
        print("Deleting vpc.... ", vpcId)
        ec2.delete_vpc(VpcId=vpcId)
    except:
        pass
