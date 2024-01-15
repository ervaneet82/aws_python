import boto3
import json

# IAM policy name
policy_name = "masteraccountcrossAccountAssumePolicy"

assume = ["arn:aws:iam::141803583963:role/customRoleForPython","arn:aws:iam::759410639220:role/codebuildforpython"]
# Define the updated policy document
updated_policy_document = {
    "Version": "2012-10-17",
    "Statement": {
        "Effect": "Allow",
        "Action": "sts:AssumeRole",
        "Resource": assume
        }
}

# Convert the updated policy document to a JSON string
updated_policy_json = json.dumps(updated_policy_document)

# Create an IAM client
iam_client = boto3.client('iam')

# Get the existing policy details
existing_policy = iam_client.get_policy(PolicyArn="arn:aws:iam::563752981057:policy/" + policy_name)

# Update the policy with the new policy document
response = iam_client.create_policy_version(
    PolicyArn=existing_policy['Policy']['Arn'],
    PolicyDocument=updated_policy_json,
    SetAsDefault=True
)

# Print the ARN of the updated policy
print(f"Updated Policy ARN: {existing_policy['Policy']['Arn']}")
