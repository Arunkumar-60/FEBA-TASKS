import boto3
region = 'ap-south-1'
instances = [''] #add instance ID required to be stopped
ec2 = boto3.client('ec2', region_name = region)

def lambda_handler(event, context):
    ec2.start_instances(InstanceIds=instances)
    print('event handeler stopped the instances' +str(instances))