import boto3
import time

region = 'ap-south-1'
instances = ['i-000c62e5118b88d8a']  # Replace with your instance ID
ec2 = boto3.client('ec2', region_name=region)

def wait_for_status_checks(instance_ids, max_wait=300, interval=15):
    """Wait for instances to pass both system and instance status checks."""
    start_time = time.time()
    while True:
        response = ec2.describe_instance_status(InstanceIds=instance_ids, IncludeAllInstances=True)
        statuses = response['InstanceStatuses']
        
        all_passed = True
        for instance in instance_ids:
            status = next((s for s in statuses if s['InstanceId'] == instance), None)
            if status:
                system_status = status['SystemStatus']['Status']
                instance_status = status['InstanceStatus']['Status']
                
                if system_status != 'ok' or instance_status != 'ok':
                    all_passed = False
                    break
            else:
                # If there's no status information for the instance
                all_passed = False
                break
        
        if all_passed:
            print('All instances have passed the status checks.')
            return True
        
        elapsed_time = time.time() - start_time
        if elapsed_time > max_wait:
            print('Timeout waiting for instances to pass status checks.')
            return False
        
        print('Waiting for instances to pass status checks...')
        time.sleep(interval)

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
    print('Checking instance status checks...')
    
    # Wait for instance status checks to pass
    if wait_for_status_checks(instances):
        print('Instance status checks passed. Checking if instances are stopped...')
        
        # Check current state of the instances
        response = ec2.describe_instances(InstanceIds=instances)
        instances_status = {instance['InstanceId']: instance['State']['Name'] for reservation in response['Reservations'] for instance in reservation['Instances']}
        
        # Stop the instances if they are not already stopped
        if any(state != 'stopped' for state in instances_status.values()):
            print('Stopping instances:', str(instances))
            ec2.stop_instances(InstanceIds=instances)
            
            # Wait until the instances are stopped
            if wait_for_instance_stopped(instances):
                print('Instances are stopped. Starting instances.')
                ec2.start_instances(InstanceIds=instances)
                print('Started instances:', str(instances))
            else:
                print('Failed to get all instances to stopped state within the timeout period.')
        else:
            print('Instances are already stopped. Starting instances.')
            ec2.start_instances(InstanceIds=instances)
            print('Started instances:', str(instances))
    else:
        print('Failed to pass status checks within the timeout period.')
