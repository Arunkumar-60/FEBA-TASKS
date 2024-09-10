# how to download all aws lambda functions

1.  install aws-cli on local machine
2.  aws configure - give configuration details
3.  run the following code

    # in terminal run commmands

    ## step - 1 : to get json file containing all the lambda functions from your aws account

        aws lambda list-functions --output json > functions.json

    ## Step -2 : Load the function list - Download the code of functions as ZIP files

    $functions = Get-Content -Raw -Path "functions.json" | ConvertFrom-Json
    $functionsList = $functions.Functions

    foreach ($function in $functionsList) {
    $functionName = $function.FunctionName

    $url = aws lambda get-function --function-name $functionName --query 'Code.Location' --output text

    if ($url) {
        $destination = "$functionName.zip"
    Invoke-WebRequest -Uri $url -OutFile $destination
    Write-Output "Downloaded $functionName to $destination"
    } else {
    Write-Output "No code URL found for $functionName"
    }
    }

    ## Step - 3 : Extract Downloaded ZIP file to obtain the python codes
