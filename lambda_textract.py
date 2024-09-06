import json
import boto3

# Initialize clients for Textract and DynamoDB
textract = boto3.client('textract',region_name='us-east-1')
dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

def lambda_handler(event, context):
    # Replace with your actual table name
    table_name = 'pdfdata'
    table = dynamodb.Table(table_name)
    
    # Assuming the document is provided via S3 trigger event
    bucket = event['Records'][0]['s3']['bucket']['name']
    document = event['Records'][0]['s3']['object']['key']
    createdat = event['Records'][0]['eventTime']
    id = event['Records'][0]['responseElements']['x-amz-request-id']
    
    # Call Textract to start the document analysis job
    response = textract.start_document_analysis(
        DocumentLocation={'S3Object': {'Bucket': bucket, 'Name': document}},
        FeatureTypes=['TABLES', 'FORMS']
    )
    
    job_id = response['JobId']
    
    # Wait for the job to complete
    job_status = ''
    while job_status != 'SUCCEEDED':
        response = textract.get_document_analysis(JobId=job_id)
        job_status = response['JobStatus']
        if job_status in ['FAILED', 'PARTIAL_SUCCESS']:
            raise Exception(f'Textract job failed with status: {job_status}')
    
    # Get the completed job results
    next_token = None
    blocks = []
    while True:
        if next_token:
            response = textract.get_document_analysis(JobId=job_id, NextToken=next_token)
        else:
            response = textract.get_document_analysis(JobId=job_id)
        blocks.extend(response['Blocks'])
        next_token = response.get('NextToken')
        if not next_token:
            break
    
    # Parse the response and extract relevant data
    key_map = {}
    value_map = {}
    block_map = {}
    
    for block in blocks:
        block_id = block['Id']
        block_map[block_id] = block
        if block['BlockType'] == "KEY_VALUE_SET":
            if 'KEY' in block['EntityTypes']:
                key_map[block_id] = block
            else:
                value_map[block_id] = block

    def get_text(result, blocks_map):
        text = ''
        if 'Relationships' in result:
            for relationship in result['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        word = blocks_map[child_id]
                        if word['BlockType'] == 'WORD':
                            text += word['Text'] + ' '
        return text.strip()

    kvs = {}
    for block_id, key_block in key_map.items():
        value_block = None
        if 'Relationships' in key_block:
            for relationship in key_block['Relationships']:
                if relationship['Type'] == 'VALUE':
                    for value_id in relationship['Ids']:
                        value_block = value_map[value_id]
                        key = get_text(key_block, block_map)
                        val = get_text(value_block, block_map)
                        kvs[key] = val
                        
    response = table.put_item(
            Item={
                'document_name': document,
                'id': id,
                'createdat': createdat,
                'data': kvs
            }
        )

    # for key, value in kvs.items():
       
    #     response = table.put_item(
    #         Item={
    #             'id': id,
    #             'document_name': document,
    #             'createdat': createdat,
    #             'key': key,
    #             'value': value
    #         }
    #     )

