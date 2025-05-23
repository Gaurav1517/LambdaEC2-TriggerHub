import boto3

def lambda_handler(event, context):
    print("Step1: Stopping EC2 instance process")
    
    ec2 = boto3.client('ec2', region_name='us-east-1')
    ec2.stop_instances(InstanceIds=['i-0015010ae14fa4fb1'])

    print("Step2: EC2 instance stopped successfully!!")
    return {
        'statusCode': 200,
        'body': 'EC2 instance stopped successfully!'
    }
