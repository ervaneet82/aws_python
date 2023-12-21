import boto3
import sys

fsx_client = boto3.client('fsx')
ec2_client = boto3.client('ec2')

response = fsx_client.describe_file_systems()

#fs_name = ""
#eni_id = ""
#sg_name = ""
try:
    for fs_instance in response['FileSystems']:
        for tags in fs_instance['Tags']:
            if tags['Key'] == 'Name':
                fs_name = tags['Value']
            eni_id = fs_instance['NetworkInterfaceIds'][0]
            sg_response = ec2_client.describe_network_interfaces(NetworkInterfaceIds=[eni_id])
            security_group_ids = sg_response['NetworkInterfaces'][0]['Groups']
            for group_id in security_group_ids:
                sg_response = ec2_client.describe_security_groups(GroupIds=[group_id['GroupId']])
                sg_name = sg_response['SecurityGroups'][0]['GroupName']
        print('{},{},{}'.format(fs_name,eni_id,sg_name))
except:
    print("Not found")
