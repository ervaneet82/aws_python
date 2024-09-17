import boto3
import csv

# Initialize a session using Amazon SecurityHub
client = boto3.client('securityhub')

# Get findings
response = client.get_findings()

# Open a CSV file for writing
with open('findings.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Title', 'Severity'])

    # Iterate through findings and write to CSV, excluding 'Info' severity
    for finding in response['Findings']:
        severity = finding['Severity']['Label']
        if severity != 'INFORMATIONAL':
            writer.writerow([finding['Title'], severity])

print("CSV file 'findings.csv' created successfully.")
