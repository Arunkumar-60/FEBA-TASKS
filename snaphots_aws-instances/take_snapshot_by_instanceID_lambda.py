import boto3
import json
import os

region_id = "ap-south-1"
instances = ['i-0d3420ecbbacdf631']  # Replace with instance IDs
ec2 = boto3.client('ec2', region_name=region_id)

def lambda_handler(event, context):
    try:
        for instance_id in instances:
            volume_ids = get_volume_ids(instance_id)
            for volume_id in volume_ids:
                create_snapshot(volume_id)
        return {
            'statusCode': 200,
            'body': json.dumps('Snapshots created successfully')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error: ' + str(e))
        }

def get_volume_ids(instance_id):
    ec2_client = boto3.client('ec2', region_name=region_id)
    volumes = ec2_client.describe_volumes(
        Filters=[
            {
                'Name': 'attachment.instance-id',
                'Values': [instance_id]
            }
        ]
    )   
    
    if not volumes['Volumes']:
        raise Exception(f'No volumes found for instance ID {instance_id}')
    
    return [volume['VolumeId'] for volume in volumes['Volumes']]

def create_snapshot(volume_id):
    response = ec2.create_snapshot(
        Description='Snapshot created by Lambda function',
        VolumeId=volume_id
    )
    print(f'Created snapshot {response["SnapshotId"]} for volume {volume_id}')
