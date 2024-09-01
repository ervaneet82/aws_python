import boto3

# Create a Service Quotas client
service_quotas = boto3.client('service-quotas')

# List service quotas for IAM
quotas = service_quotas.list_service_quotas(ServiceCode='iam')

# Print all quotas for IAM
for quota in quotas['Quotas']:
    if quota['Value'] == 10 and 'Managed' in quota['QuotaName']:
        print(f"{quota['QuotaName']}, {quota['Value']}, {quota['QuotaCode']}")
        response = service_quotas.request_service_quota_increase(
                ServiceCode='iam',
                QuotaCode=quota['QuotaCode'],
                DesiredValue=20
                )
        print(f"Requested Quota Increase: {response['RequestedQuota']['DesiredValue']}")
