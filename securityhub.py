import boto3
from datetime import datetime, timedelta
import csv

# Initialize a SecurityHub client
client = boto3.client('securityhub')

# Calculate the time 2 hours ago from the current time
two_hours_ago = datetime.now() - timedelta(hours=2)
two_hours_ago_str = two_hours_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
now_str = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

# Get the account ID from the current credentials
account_id = boto3.client('sts').get_caller_identity().get('Account')

# Function to fetch findings with pagination
def fetch_findings():
    findings = []
    paginator = client.get_paginator('get_findings')
    page_iterator = paginator.paginate(
        Filters={
            'RecordState': [{
                'Value': 'ACTIVE',
                'Comparison': 'EQUALS'
            }],
            'SeverityLabel': [{
                'Value': 'INFORMATIONAL',
                'Comparison': 'NOT_EQUALS'
            }],
            'UpdatedAt': [{
                'Start': two_hours_ago_str,
                'End': now_str
            }]
        }
    )
    for page in page_iterator:
        findings.extend(page['Findings'])
    return findings

# Fetch the findings
findings = fetch_findings()
sorted_findings = sorted(findings, key=lambda x: x.get('Title', ''))

# Write findings to CSV
with open('security_hub_findings.csv', 'w', newline='') as file:
    fieldnames = ['AccountId', 'Title', 'Description', 'Severity', 'UpdatedAt']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for finding in sorted_findings:
        writer.writerow({
            'AccountId': account_id,
            'Title': finding.get('Title', ''),
            'Description': finding.get('Description', ''),
            'Severity': finding.get('Severity', {}).get('Label', ''),
            'UpdatedAt': finding.get('UpdatedAt', '')
        })

print("CSV file has been created with the findings.")
