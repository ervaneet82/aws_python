import boto3

def lambda_handler(event, context):
    # Replace 'YourPipelineName' with the actual name of your CodePipeline
    pipeline_name = '2073320-pipeline'

    # Create a CodePipeline client
    codepipeline_client = boto3.client('codepipeline')

    try:
        # Get the latest execution of the specified pipeline
        response = codepipeline_client.list_pipeline_executions(
            pipelineName=pipeline_name,
            maxResults=1
        )

        if 'pipelineExecutionSummaries' in response and response['pipelineExecutionSummaries']:
            latest_execution = response['pipelineExecutionSummaries'][0]
            status = latest_execution['status']
            print(f"Latest execution status: {status}")

            # You can perform additional actions based on the status
            if status == 'Succeeded':
                print("Pipeline execution succeeded")
            elif status == 'Failed':
                print("Pipeline execution failed")
            else:
                print("Pipeline execution is still in progress")

            return status

    except Exception as e:
        print(f"Error checking pipeline status: {str(e)}")
        return "Error"

    return "Unknown"

