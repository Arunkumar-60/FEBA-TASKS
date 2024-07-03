**Instructions to make the automated snapshot with lifespan in AWS (for
backup).**

# non-admin (IAM user):
## policies:
policy.json

create a role , with name (snapshot_role_for_lambda)
<!-- polices are to be updated and json format for policies are yet to be updated -->


**[PROCEDURE:]{.underline}**



**Steps to Launch an Instance and Automate Snapshot Creation with
Lambda**

**1. Launch an EC2 Instance**

-   Launch an EC2 instance with your required configurations.

    > Ensure that the instance has one or multiple volumes.

    > Take snapshots of every volume attached to the instance.

**2. Create an IAM Policy**

-   **Name:** Choose a name for the policy (e.g., EC2LambdaPolicy).

    > **Policies to Add:**

    1.  EC2 Full Access Policy

    2.  Lambda Basic Execution Policy

**3. Create the Lambda Function**

1.  **Function Name:** Choose a name for the function.

2.  **Runtime Language:** Select Python 3.12 or a lower version.

3.  **Execution Role:** Change the default execution role to use an
    > existing role and select the role created in Step 2.

4.  **Create the Function.**

**4. Add Code to Lambda Function**

-   Copy the following Python code into the Lambda function code page.

    > Replace your_instance_id with your own instance ID.

    > Save changes and deploy.

**5. Configure a Test Event**

1.  **Create New Event:**

    -   Select the option to configure a test event from the dropdown
        > menu.

2.  **Event Name:** Enter a name for your test event and save.

3.  **Test the Function:**

    -   Click on the test button to check the functionality of the
        > Lambda function.

4.  **Verify Execution:**

    -   Check the Snapshots page in the EC2 console to see the newly
        > created snapshots.

**6. Schedule the Event to Trigger the Lambda Function**

1.  **Go to Amazon EventBridge.**

2.  **Under the Schedules Section:**

    -   Create a new schedule.

3.  **Schedule Name:** Enter a name for the schedule.

4.  **Description:** Write a description (optional).

5.  **Design Your Schedule Pattern:**

    -   Choose a recurring schedule to trigger the function weekly.

6.  **Under Recurring Schedule (Rate-Based Schedule):**

    -   Set the frequency of triggering the Lambda function.

7.  **Select Flexible Time Window:** Set to 5 minutes or off.

8.  **Templated Target:** Choose AWS Lambda and select the Lambda
    > function.

9.  **Create Schedule.**
