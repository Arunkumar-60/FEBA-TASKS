# safe start instance methodology:

Check the Instance State: Use describe_instances to check the current state of the instance.
Wait Until the Instance is Stopped: If the instance is not in the stopped state, wait until it is.
Start the Instance: Once the instance is in the stopped state, start it.

# safe stop instance methodology:

Wait for Status Checks: Use the describe_instance_status method to ensure that both status checks have passed.
Stop the Instance: Use the stop_instances method once the instance is ready.
