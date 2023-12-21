import boto3

def describe_fsx_instances():
    # Create an FSx client
    fsx_client = boto3.client('fsx')

    # Describe FSx instances
    response = fsx_client.describe_file_systems()

    # Iterate through each FSx instance
    for fs_instance in response['FileSystems']:
        # Extract relevant information
        fs_name = fs_instance['FileSystemId']
        eni_ids = [eni['NetworkInterfaceIds'][0] for eni in fs_instance['NetworkInterfaceIds']]
        security_group_ids = fs_instance['SecurityGroupIds']

        # Print information
        print(f"File System Name: {fs_name}")
        print(f"Associated ENI IDs: {eni_ids}")
        print(f"Security Group IDs: {security_group_ids}")
        print("\n")

if __name__ == "__main__":
    describe_fsx_instances()

import boto3

def describe_eni_security_groups(eni_id):
    # Create EC2 client
    ec2_client = boto3.client('ec2')

    # Describe the ENI
    response = ec2_client.describe_network_interfaces(NetworkInterfaceIds=[eni_id])

    # Extract security group IDs associated with the ENI
    security_group_ids = response['NetworkInterfaces'][0]['Groups']

    # Extract security group names using the security group IDs
    security_group_names = []
    for group_id in security_group_ids:
        sg_response = ec2_client.describe_security_groups(GroupIds=[group_id['GroupId']])
        security_group_names.append(sg_response['SecurityGroups'][0]['GroupName'])

    return security_group_names

if __name__ == "__main__":
    # Replace 'your_eni_id' with the actual ENI ID
    eni_id = 'your_eni_id'

    # Get security group names associated with the ENI
    sg_names = describe_eni_security_groups(eni_id)

    # Print the results
    print(f"Security Group Names associated with ENI {eni_id}: {sg_names}")

