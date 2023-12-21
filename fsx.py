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
