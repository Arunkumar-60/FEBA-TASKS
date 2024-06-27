import boto3
import json
import time

region_id = "ap-south-1"
instances = [''] #instance ID goes here
ec2 = boto3.client('ec2', region_name=region_id)

def lambda_handler(event, context):
    try:
        for instance_id in instances:
            stop_instance(instance_id)
            wait_for_instance(instance_id, 'stopped')
            
            volume_ids = get_volume_ids(instance_id)
            snapshot_ids = []
            for volume_id in volume_ids:
                snapshot_id = create_snapshot(volume_id)
                snapshot_ids.append(snapshot_id)
            
            wait_for_snapshots(snapshot_ids)
            
            start_instance(instance_id)
            wait_for_instance(instance_id, 'running')
        
        return {
            'statusCode': 200,
            'body': json.dumps('Snapshots created and instance restarted successfully')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error: ' + str(e))
        }

def stop_instance(instance_id):
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f'Stopping instance {instance_id}')

def start_instance(instance_id):
    ec2.start_instances(InstanceIds=[instance_id])
    print(f'Starting instance {instance_id}')

def wait_for_instance(instance_id, state):
    waiter = ec2.get_waiter(f'instance_{state}')
    waiter.wait(InstanceIds=[instance_id])
    print(f'Instance {instance_id} is now {state}')

def get_volume_ids(instance_id):
    volumes = ec2.describe_volumes(
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
        Description='Phase-1 of automating snapshots(checking execution policies)',
        VolumeId=volume_id
    )
    snapshot_id = response["SnapshotId"]
    print(f'Created snapshot {snapshot_id} for volume {volume_id}')
    return snapshot_id

def wait_for_snapshots(snapshot_ids):
    for snapshot_id in snapshot_ids:
        waiter = ec2.get_waiter('snapshot_completed')
        waiter.wait(SnapshotIds=[snapshot_id])
        print(f'Snapshot {snapshot_id} is now completed')
