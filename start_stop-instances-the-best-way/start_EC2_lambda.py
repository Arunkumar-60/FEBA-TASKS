import boto3
import time

region = 'ap-south-1'
instances = ['i-000c62e5118b88d8a'] # replace your instance id
ec2 = boto3.client('ec2', region_name=region)

def wait_for_instance_stopped(instance_ids, max_wait=300, interval=15):
    """Wait until all instances are in the 'stopped' state."""
    start_time = time.time()
    while True:
        response = ec2.describe_instances(InstanceIds=instance_ids)
        reservations = response['Reservations']
        instances_status = {instance_id: 'unknown' for instance_id in instance_ids}
        
        for reservation in reservations:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                state = instance['State']['Name']
                instances_status[instance_id] = state
        
        if all(state == 'stopped' for state in instances_status.values()):
            print('All instances are stopped.')
            return True
        
        elapsed_time = time.time() - start_time
        if elapsed_time > max_wait:
            print('Timeout waiting for instances to reach stopped state.')
            return False
        
        print('Waiting for instances to be stopped...')
        time.sleep(interval)

def lambda_handler(event, context):
    # Check if instances are stopped, wait if not
    if wait_for_instance_stopped(instances):
        print('Starting instances:', str(instances))
        ec2.start_instances(InstanceIds=instances)
        print('Started instances:', str(instances))
    else:
        print('Failed to get all instances to stopped state within the timeout period.')

