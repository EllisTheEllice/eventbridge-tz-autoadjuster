# What is the purpose of this project?

See [this blog article](https://www.cloud4engineers.com/posts/2021/11/automatically-adjust-aws-eventbridge-timezones/) for details on the background and purpose of this project.

# Prerequisites

## 1. Create a S3 bucket to upload CloudFormation artifacts

CloudFormation requires a S3 bucket for uploading the generated files. This has to be created manually by following [these steps](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html). Note down the S3 bucket name, as this will be required during setup.

## 2. Create an IAM user and role to execute the stack

The deployment scripts use an IAM user with a role assigned to create the infrastructure. So follow [these steps](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html) to create a new IAM user with a policy attached. Make sure you add the following permissions to the policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "lambda:CreateFunction",
                "lambda:DeleteFunction",
                "lambda:AddPermission",
                "lambda:GetFunction",
                "lambda:GetFunctionConfiguration",
                "lambda:UpdateFunctionCode",
                "lambda:UpdateFunctionConfiguration",
                "cloudformation:*",
                "events:DeleteRule",
                "events:DescribeRule",
                "events:EnableRule",
                "events:ListRules",
                "events:PutEvents",
                "events:PutRule",
                "events:PutTargets",
                "events:RemoveTargets",
                "iam:AttachRolePolicy",
                "iam:CreatePolicy",
                "iam:CreatePolicyVersion",
                "iam:CreateRole",
                "iam:CreateServiceLinkedRole",
                "iam:DeletePolicy",
                "iam:DeletePolicyVersion",
                "iam:DeleteRole",
                "iam:DeleteRolePolicy",
                "iam:DeleteServiceLinkedRole",
                "iam:DetachRolePolicy",
                "iam:GetPolicy",
                "iam:PassRole",
                "iam:GetRole",
                "iam:PutRolePolicy",
                "s3:*"
            ],
            "Resource": "*"
        }
    ]
}
```

Not down the role??s arn as you will need it in the next step.
After you??ve set up the user, follow [these steps](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html) to create a named profile. This will be used during deployment later.

Now you have created a role with a policy attached. Do these steps also to create a role. Make sure you specify cloudformation as the service which can assume this role (principal). You can attach the same policy to it. Note down the role??s  ARN.


## 3. Replace placeholders in deploy_script.ps1

If you are executing the stack from within a Windows environment, you can use the deploy_script.ps1 to do so. There are some placeholders in the file which you have to replace with actual values first:

![](/doc/images/deploy_script.PNG)


## 4. Fill config/qa.json with values (optional)

If you want to allow cross-function access to the lambda function, you have to specify the account id in the config/qa.json file.

## 5. Install aws cli

The machine executing the CloudFormation script requires the AWS cli to be installed. Follow [these steps](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) to install the cli.

# How to deploy?

If you followed the steps above, all you need to do is to execute the deploy_script.ps1 with Powershell. If you are in a Linux-based environment, you should use the deploy_script.sh instead.
