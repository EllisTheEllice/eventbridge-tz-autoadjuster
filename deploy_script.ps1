### Log in to the account via commandline login
$stage= "qa"
$aws_profile="<YOUR_PROFILE>"
# Change parameters depending on Stage
if ($stage.Equals("qa")) {
    ## DEV
    $stackname = "timezone-auto-adjuster"
    $configfile = "file://config/qa.json"
    $bucketname = "<YOUR_BUCKET_NAME>"
    $cfn_role = "<YOUR_ROLE_ARN>"
}else {
    Write-Output "Please enter a valid stage --> EXIT."
    break
}

aws cloudformation package --template-file infrastructure.yaml --s3-bucket $bucketname --output-template-file packaged_infrastructure.yaml --profile $aws_profile

# ` will require always a protruding space for the next parameter
aws cloudformation deploy --template-file packaged_infrastructure.yaml `
    --stack-name $stackname `
    --parameter-overrides $configfile `
    --capabilities CAPABILITY_NAMED_IAM `
    --role-arn $cfn_role --profile $aws_profile
