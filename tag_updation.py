import re
import boto3
import sys

# s = "APM3457"
# fill_zeros = 10 - len(s)

session = boto3.Session(profile_name='463257850487_PowerUserAccess', region_name='us-east-1')
ec2 = session.client('ec2')
#s3 = boto3.client('s3')
#id = boto3.client('sts').get_caller_identity().get('Account')

response = ec2.describe_instances()
for reservation in response['Reservations']:
  for instances in reservation['Instances']:
    print(instances['InstanceId'])
    for items in instances['Tags']:
      if items['Key'] == 'CE_Application_ID':
        if re.match(r'^APM\d{10}$', items['Value']):
          print(items['Value'])
        else:
          print("No Matching the pattern", items['Value'])
          if len(items['Value']) < 10:
            fill_zeros = 10 - len(items['Value'])
            d = ''.join(re.findall('\d+', items['Value']))
            s1 = ''.join(re.findall('[aA-zZ]+', items['Value']))
            zero_padding = len(d) + fill_zeros
            new_str = s1 + d.zfill(7)
            print(new_str)
            print(len(new_str))
            ec2.delete_tags(Resources=[instances['InstanceId']], Tags=[{"Key": "CE_Application_ID" }])
            response = ec2.create_tags(
              Resources=[instances['InstanceId']],
              Tags=[
                {
                  'Key': 'CE_Application_ID',
                  'Value': new_str
                }
              ]
            )
