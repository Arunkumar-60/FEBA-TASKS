import boto3
import json
from datetime import datetime, timedelta, timezone

time = 20 # in minutes
instance_ids = ['i-0d3420ecbbacdf631']  # Replace with your instance IDs

# change region_ID if necessary
region_id = "ap-south-1"

ec2 = boto3.client('ec2', region_name=region_id)

def lambda_handler(event, context):
    try:
        volume_ids = get_attached_volume_ids(instance_ids)
        delete_old_snapshots(volume_ids)
        return {
            'statusCode': 200,
            'body': json.dumps('Old snapshots deleted successfully')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('Error: ' + str(e))
        }

def get_attached_volume_ids(instance_ids):
    volume_ids = []
    for instance_id in instance_ids:
        volumes = ec2.describe_volumes(
            Filters=[
                {
                    'Name': 'attachment.instance-id',
                    'Values': [instance_id]
                }
            ]
        )['Volumes']
        
        for volume in volumes:
            volume_ids.append(volume['VolumeId'])
    
    return volume_ids

def delete_old_snapshots(volume_ids):
    time_threshold = datetime.now(timezone.utc) - timedelta(minutes=time)
    # time_threshold = datetime.now(timezone.utc) - timedelta(days=time) #time is to be mentioned in days
    
    
    for volume_id in volume_ids:
        # List all snapshots for the given volume ID
        snapshots = ec2.describe_snapshots(
            Filters=[
                {
                    'Name': 'volume-id',
                    'Values': [volume_id]
                }
            ]
        )['Snapshots']
        
        # Filter and delete snapshots older than the required time
        for snapshot in snapshots:
            if snapshot['StartTime'] < time_threshold:
                ec2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                print(f'Deleted snapshot {snapshot["SnapshotId"]} for volume {volume_id}')

