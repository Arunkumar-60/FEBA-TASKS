import boto3
import time

region = 'ap-south-1'
instances = ['i-000c62e5118b88d8a'] # replace your instance ID
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

def lambda_handler(event, context):
    # Wait for instances to pass status checks
    if wait_for_status_checks(instances):
        print('Instances have passed the status checks. Stopping instances.')
        ec2.stop_instances(InstanceIds=instances)
        print('Stopped instances:', str(instances))
    else:
        print('Failed to pass status checks within the timeout period.')

