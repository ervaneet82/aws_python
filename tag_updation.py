import re
import boto3
import sys

session = boto3.Session(profile_name='463257850487_PowerUserAccess', region_name='us-east-1')
ec2 = session.client('ec2')
s3 = session.client('s3')
rds = boto3.client('rds')
#id = boto3.client('sts').get_caller_identity().get('Account')

def tagging(value):
    fill_zeros = 10 - len(value)
    d = ''.join(re.findall('\d+', value))
    s1 = ''.join(re.findall('[aA-zZ]+', value))
    zero_padding = len(d) + fill_zeros
    new_str = s1 + d.zfill(zero_padding)
    return new_str

def ec2_tagging_fix():
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
      for instances in reservation['Instances']:
        for items in instances['Tags']:
          if items['Key'] == 'Application_ID':
            if re.match(r'^APM\d{7}$', items['Value']):
                print(items['Value'])
            else:
                if len(items['Value']) < 10:
                    new_str = tagging(items['Value'])
                    ec2.delete_tags(
                      Resources=[instances['InstanceId']],
                      Tags=[{"Key": "Application_ID"}]
                    )
                    print("updating tags")
                    ec2.create_tags(
                      Resources=[instances['InstanceId']],
                      Tags=[
                        {
                          'Key': 'Application_ID',
                          'Value': new_str
                        }
                      ]
                    )
                    break

def s3_tagging_fix():
    response = s3.list_buckets()['Buckets']
    for bucket in response:
        for tag in s3.get_bucket_tagging(Bucket=bucket['Name'])['TagSet']:
            if tag['Key'] == 'Application_ID':
                if not re.match(r'^APM\d{7}$', tag['Value']):
                    print("Tag Value of {} is {}".format(bucket['Name'], tag['Value']))
                if re.match(r'^APM', tag['Value']) and len(tag['Value']) < 10:
                    new_str = tagging(tag['Value'])
                    print("updating tags value {} from {} to {}".format(bucket['Name'], tag['Value'], new_str))
                    s3.put_bucket_tagging(
                        Bucket=bucket['Name'],
                        Tagging={
                          'TagSet': [
                            {
                              'Key': 'Application_ID',
                              'Value': new_str
                            }
                          ]
                        }
                    )
                    break

def rds_tagging_fix():
  db = rds.describe_db_instances()['DBInstances']


#ec2_tagging_fix()
s3_tagging_fix()
