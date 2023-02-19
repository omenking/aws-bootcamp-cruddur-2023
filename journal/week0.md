# Week 0 — Billing and Architecture

## Required Homework

### Install AWS CLI

I have installed the CLI within GitPod and on a local linux VM installation. Here is the CLI showing that AWS CLI is installed and working:

ivorypalace@pop-os:~$ aws --version
aws-cli/2.10.1 Python/3.9.11 Linux/6.0.12-76060006-generic exe/x86_64.pop.22 prompt/off

![image](https://user-images.githubusercontent.com/123283155/219908859-28a07902-363b-4101-af61-cd40e57e54b3.png)
![image](https://user-images.githubusercontent.com/123283155/219909101-07c6b9fd-72b7-455e-a6c9-e63369ba5eee.png)

## Created Lucid Charts 

Followed the Videos and created Lucid Charts and **updated** Lucid Charts video
![image](/asset/"Architecting and Billing.png")
![image](https://user-images.githubusercontent.com/123283155/219923075-f59dda72-5588-4970-ab33-0a541e5c8548.png)

## Setup AWS Budget and Billing Accounts

Went through AWS CloudShell to get the following JSON on my budget:
![image](https://user-images.githubusercontent.com/123283155/219910296-5d15b9da-90ea-4363-9ef9-d6354bc3403d.png)

Then performed the same within the AWS CLI:
![image](https://user-images.githubusercontent.com/123283155/219911457-8e649193-17f5-42f2-9fee-612698ff4c6c.png)

Here is the information for my Billing Alarms from AWS:
{
    "Type": "AWS::CloudWatch::Alarm",
    "Properties": {
        "AlarmName": "Billing Alert",
        "ActionsEnabled": true,
        "OKActions": [],
        "AlarmActions": [
            "arn:aws:sns:us-east-1:218164361575:Default_CloudWatch_Alarms_Topic"
        ],
        "InsufficientDataActions": [],
        "MetricName": "AWS BootCamp Billing Alert",
        "Namespace": "AWS/Billing",
        "Statistic": "Maximum",
        "Dimensions": [
            {
                "Name": "Currency",
                "Value": "USD"
            }
        ],
        "Period": 21600,
        "EvaluationPeriods": 1,
        "DatapointsToAlarm": 1,
        "Threshold": 10,
        "ComparisonOperator": "GreaterThanThreshold",
        "TreatMissingData": "missing"
    }
}
