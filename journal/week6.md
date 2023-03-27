# Week 6 — Deploying Containers

## Test RDS Connecetion

Add this `test` script into `db` so we can easily check our connection from our container.

```sh
#!/usr/bin/env python3

import psycopg
import os
import sys

connection_url = os.getenv("CONNECTION_URL")

conn = None
try:
  print('attempting connection')
  conn = psycopg.connect(connection_url)
  print("Connection successful!")
except psycopg.Error as e:
  print("Unable to connect to the database:", e)
finally:
  conn.close()
```

## Task Flask Script

We'll add the following endpoint for our flask app:

```py
@app.route('/api/health-check')
def health_check():
  return {'success': True}, 200
```

We'll create a new bin script at `bin/flask/health-check`

```py
#!/usr/bin/env python3

import urllib.request

response = urllib.request.urlopen('http://localhost:4567/api/health-check')
if response.getcode() == 200:
  print("Flask server is running")
else:
  print("Flask server is not running")
```

### NAT Instance

VNS3 NATe Free (NAT Gateway Appliance)

https://aws.amazon.com/marketplace/pp/prodview-wf7yma4f6mdw4#pdp-usage


### Create a subnet just for the NAT

Lets see all the avaliable AZs
```sh
aws ec2 describe-availability-zones \
  --region $AWS_DEFAULT_REGION \
  --query 'AvailabilityZones[].ZoneName' \
  --output table
```

```sh
aws ec2 create-subnet \
--vpc-id $DEFAULT_VPC_ID \
--cidr-block 172.31.48.0/20 \
--availability-zone ca-central-1a \
--tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=subnet-nat-main}]'
```

### Create three new subnets for the NAT

```sh
export SUBNET_NAT_A=$(aws ec2 create-subnet \
--vpc-id $DEFAULT_VPC_ID \
--cidr-block '172.31.64.0/20' \
--availability-zone ca-central-1a \
--tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=subnet-nat-a}]' \
--query 'Subnet.SubnetId' \
--output text)
echo $SUBNET_NAT_A
```

```sh
export SUBNET_NAT_B=$(aws ec2 create-subnet \
--vpc-id $DEFAULT_VPC_ID \
--cidr-block '172.31.80.0/20' \
--availability-zone ca-central-1b \
--tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=subnet-nat-b}]' \
--query 'Subnet.SubnetId' \
--output text)
echo $SUBNET_NAT_B
```

```sh
export SUBNET_NAT_D=$(aws ec2 create-subnet \
--vpc-id $DEFAULT_VPC_ID \
--cidr-block '172.31.96.0/20' \
--availability-zone ca-central-1d \
--tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=subnet-nat-d}]' \
--query 'Subnet.SubnetId' \
--output text)
echo $SUBNET_NAT_D
```

> probably don't need these
```sh
aws ec2 modify-subnet-attribute --subnet-id $SUBNET_NAT_A --map-public-ip-on-launch
aws ec2 modify-subnet-attribute --subnet-id $SUBNET_NAT_B --map-public-ip-on-launch
aws ec2 modify-subnet-attribute --subnet-id $SUBNET_NAT_D --map-public-ip-on-launch
```

### Create the NAT Instance

We'll need to create a NAT Instance for the EC2 Marketplace for the
VNS3 NATe Free (NAT Gateway Appliance)

Once created we need to get its ENI, and we'll create a Route Table that sends `0.0.0.0/0` to that Appliance ENI 

## Create CloudWatch Log Group

```sh
aws logs create-log-group --log-group-name cruddur
aws logs put-retention-policy --log-group-name cruddur --retention-in-days 1
```

## Create ECS Cluster

```sh
aws ecs create-cluster \
--cluster-name cruddur \
--service-connect-defaults namespace=cruddur
```

## Create Launch Template

### Get ECS Opitmized EC2 AMI

Get the ECS-optimized AMI for my default region

```sh
export ECS_OPTIMIZED_AMI=$(aws ec2 describe-images \
--owner amazon \
--filters "Name=description,Values=\"*Amazon Linux AMI 2.0.20230109 x86_64 ECS HVM GP2*\"" \
--query "Images[?ImageLocation=='amazon/amzn2-ami-ecs-hvm-2.0.20230109-x86_64-ebs'].ImageId" \
--output text)
```

### Create UserData script that will configure ECS
Base64 encode launching the cluster

```sh
echo '#!/bin/bash\necho "ECS_CLUSTER=cruddur" >> /etc/ecs/ecs.config' | base64 -w 0
```


### Create Instance Profile

We want to be able to shell into the EC2 instance incase for debugging
so we'll want to do this via Sessions Manager.

We'll create an Instance Profile with the needed permissions.

```sh
aws iam create-role --role-name session-manager-role --assume-role-policy-document "{
    \"Version\": \"2012-10-17\",
    \"Statement\": [
        {
            \"Effect\": \"Allow\",
            \"Principal\": {
                \"Service\": \"ec2.amazonaws.com\"
            },
            \"Action\": \"sts:AssumeRole\"
        }
    ]
}"
```

```sh
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role --role-name session-manager-role
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerServiceforEC2Role --role-name session-manager-role
export ECS_INSTANCE_PROFILE_ARN=$(aws iam create-instance-profile --instance-profile-name cruddur-instance-profile --query InstanceProfile.Arn)
aws iam add-role-to-instance-profile --instance-profile-name cruddur-instance-profile --role-name session-manager-role
```

Get instance profile arn after creation
```sh
export ECS_INSTANCE_PROFILE_ARN=$(aws iam get-instance-profile \
--instance-profile-name cruddur-instance-profile \
--query 'InstanceProfile.Arn' \
--output text)
```


### Create Launch Template Security Group

We need the default VPC ID
```sh
export DEFAULT_VPC_ID=$(aws ec2 describe-vpcs \
--filters "Name=isDefault, Values=true" \
--query "Vpcs[0].VpcId" \
--output text)
echo $DEFAULT_VPC_ID
```

Create 
```sh
export CRUD_CLUSTER_SG=$(aws ec2 create-security-group \
  --group-name cruddur-ecs-cluster-sg \
  --description "Security group for Cruddur ECS ECS cluster" \
  --vpc-id $DEFAULT_VPC_ID \
  --query "GroupId" --output text)
echo $CRUD_CLUSTER_SG
```

Get the Group ID (after its created)

```sh
export CRUD_CLUSTER_SG=$(aws ec2 describe-security-groups \
--group-names cruddur-ecs-cluster-sg \
--query 'SecurityGroups[0].GroupId' \
--output text)
```

### Create Launch Template

WE NEED TO HAVE A KEY PAIR SET.
We can using Sessions Manager without incurring cost when we use the NAT instance.

```sh
aws ec2 create-launch-template \
--launch-template-name cruddur-lt \
--version-description "Launch Template for Cruddur ECS EC2 Cluster" \
--launch-template-data "{
    \"ImageId\": \"$ECS_OPTIMIZED_AMI\",
    \"InstanceType\": \"t3.micro\",
    \"SecurityGroupIds\": [\"$CRUD_CLUSTER_SG\"],
    \"IamInstanceProfile\": {
        \"Arn\": \"$ECS_INSTANCE_PROFILE_ARN\"
    },
    \"UserData\": \"$(printf '#!/bin/bash\necho "ECS_CLUSTER=cruddur" >> /etc/ecs/ecs.config' | base64 -w 0)\"
}"
```

## Create ASG

We need an Auto Scaling Group so that if we need to add more EC2 instance we have the capacity to run them.


### Get Subnet Ids as commans

We need the subnet ids for both when we launch the container service but for the ASG

```sh
export DEFAULT_SUBNET_IDS=$(aws ec2 describe-subnets  \
 --filters Name=vpc-id,Values=$DEFAULT_VPC_ID \
 --query 'Subnets[*].SubnetId' \
 --output json | jq -r 'join(",")')
echo $DEFAULT_SUBNET_IDS
```

### Create the ASG
```sh
aws autoscaling create-auto-scaling-group \
--auto-scaling-group-name cruddur-asg \
--launch-template "LaunchTemplateName=cruddur-lt,Version=\$Latest" \
--min-size 1 \
--max-size 1 \
--desired-capacity 1 \
--vpc-zone-identifier $DEFAULT_SUBNET_IDS
```

## Debugging association of EC2 Instance with Cluster (optional)

If we don't see out EC2 instance associated with our cluster.
We can use sessions manger to login.

```sh
sudo su - ec2-user
/etc/ecs/ecs.config
cat /etc/ecs/ecs.config
systemctl status ecs
```

Consider that we have access to docker and we can see any running containers or shell into them eg:

```
docker ps
docker exec -it <container name> /bin/bash
```

## Create ECR repo and push image

### Login to ECR

```sh
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"
```

### For Base-image python

```sh
aws ecr create-repository \
  --repository-name cruddur-python \
  --image-tag-mutability MUTABLE
```

#### Set URL

```sh
export ECR_PYTHON_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/cruddur-python"
echo $ECR_PYTHON_URL
```

#### Pull Image

```sh
docker pull python:3.10-slim-buster
```

#### Tag Image

```sh
docker tag python:3.10-slim-buster $ECR_PYTHON_URL:3.10-slim-buster
```

#### Push Image

```sh
docker push $ECR_PYTHON_URL:3.10-slim-buster
```

### For Flask

In your flask dockerfile update the from to instead of using DockerHub's python image
you use your own eg.

> remember to put the :latest tag on the end

#### Create Repo
```sh
aws ecr create-repository \
  --repository-name backend-flask \
  --image-tag-mutability MUTABLE
```

#### Set URL

```sh
export ECR_BACKEND_FLASK_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/backend-flask"
echo $ECR_BACKEND_FLASK_URL
```

#### Build Image
```sh
docker build -t backend-flask .
```

#### Tag Image

```sh
docker tag backend-flask:latest $ECR_BACKEND_FLASK_URL:latest
```

#### Push Image

```sh
docker push $ECR_BACKEND_FLASK_URL:latest
```

### For Frontend React

#### Create Repo
```sh
aws ecr create-repository \
  --repository-name frontend-react-js \
  --image-tag-mutability MUTABLE
```

#### Set URL

```sh
export ECR_FRONTEND_REACT_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/frontend-react-js"
echo $ECR_FRONTEND_REACT_URL
```

#### Build Image

```sh
docker build \
--build-arg REACT_APP_BACKEND_URL="https://4567-$GITPOD_WORKSPACE_ID.$GITPOD_WORKSPACE_CLUSTER_HOST" \
--build-arg REACT_APP_AWS_PROJECT_REGION="$AWS_DEFAULT_REGION" \
--build-arg REACT_APP_AWS_COGNITO_REGION="$AWS_DEFAULT_REGION" \
--build-arg REACT_APP_AWS_USER_POOLS_ID="ca-central-1_CQ4wDfnwc" \
--build-arg REACT_APP_CLIENT_ID="5b6ro31g97urk767adrbrdj1g5" \
-t frontend-react-js \
-f Dockerfile.prod \
.
```

#### Tag Image

```sh
docker tag frontend-react-js:latest $ECR_FRONTEND_REACT_URL:latest
```

#### Push Image

```sh
docker push $ECR_FRONTEND_REACT_URL:latest
```


If you want to run and test it

```sh
docker run --rm -p 3000:3000 -it frontend-react-js 
```

## Register Task Defintions

### Passing Senstive Data to Task Defintion

https://docs.aws.amazon.com/AmazonECS/latest/developerguide/specifying-sensitive-data.html
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/secrets-envvar-ssm-paramstore.html

```sh
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/AWS_ACCESS_KEY_ID" --value $AWS_ACCESS_KEY_ID
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/AWS_SECRET_ACCESS_KEY" --value $AWS_SECRET_ACCESS_KEY
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/CONNECTION_URL" --value $PROD_CONNECTION_URL
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/ROLLBAR_ACCESS_TOKEN" --value $ROLLBAR_ACCESS_TOKEN
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/OTEL_EXPORTER_OTLP_HEADERS" --value "x-honeycomb-team=$HONEYCOMB_API_KEY"
```

### Create Task and Exection Roles for Task Defintion


#### Create ExecutionRole

```sh
aws iam create-role \
    --role-name CruddurServiceExecutionRole \
    --assume-role-policy-document "{
  \"Version\":\"2012-10-17\",
  \"Statement\":[{
    \"Action\":[\"sts:AssumeRole\"],
    \"Effect\":\"Allow\",
    \"Principal\":{
      \"Service\":[\"ecs-tasks.amazonaws.com\"]
    }
  }]
}"
```

```json

       {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "ssm:GetParameter",
            "Resource": "arn:aws:ssm:ca-central-1:387543059434:parameter/cruddur/backend-flask/*"
        }

```sh
aws iam attach-role-policy \
    --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy \
    --role-name CruddurServiceExecutionRole
```

```json
{
  "Sid": "VisualEditor0",
  "Effect": "Allow",
  "Action": [
    "ssm:GetParameters",
    "ssm:GetParameter"
  ],
  "Resource": "arn:aws:ssm:ca-central-1:387543059434:parameter/cruddur/backend-flask/*"
}
```

#### Create TaskRole

```sh
aws iam create-role \
    --role-name CruddurTaskRole \
    --assume-role-policy-document "{
  \"Version\":\"2012-10-17\",
  \"Statement\":[{
    \"Action\":[\"sts:AssumeRole\"],
    \"Effect\":\"Allow\",
    \"Principal\":{
      \"Service\":[\"ecs-tasks.amazonaws.com\"]
    }
  }]
}"

aws iam put-role-policy \
  --policy-name SSMAccessPolicy \
  --role-name CruddurTaskRole \
  --policy-document "{
  \"Version\":\"2012-10-17\",
  \"Statement\":[{
    \"Action\":[
      \"ssmmessages:CreateControlChannel\",
      \"ssmmessages:CreateDataChannel\",
      \"ssmmessages:OpenControlChannel\",
      \"ssmmessages:OpenDataChannel\"
    ],
    \"Effect\":\"Allow\",
    \"Resource\":\"*\"
  }]
}
"

aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/CloudWatchFullAccess --role-name CruddurTaskRole
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess --role-name CruddurTaskRole
```

### Create Json file
Create a new folder called `aws/task-defintions` and place the following files in there:

`backend-flask.json`

```json
{
  "family": "backend-flask",
  "executionRoleArn": "arn:aws:iam::AWS_ACCOUNT_ID:role/CruddurServiceExecutionRole",
  "taskRoleArn": "arn:aws:iam::AWS_ACCOUNT_ID:role/CruddurTaskRole",
  "networkMode": "awsvpc",
  "containerDefinitions": [
    {
      "name": "backend-flask",
      "image": "BACKEND_FLASK_IMAGE_URL",
      "cpu": 256,
      "memory": 512,
      "essential": true,
      "portMappings": [
        {
          "name": "backend-flask",
          "containerPort": 4567,
          "protocol": "tcp", 
          "appProtocol": "http"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
            "awslogs-group": "cruddur",
            "awslogs-region": "ca-central-1",
            "awslogs-stream-prefix": "backend-flask"
        }
      },
      "environment": [
        {"name": "OTEL_SERVICE_NAME", "value": "backend-flask"},
        {"name": "OTEL_EXPORTER_OTLP_ENDPOINT", "value": "https://api.honeycomb.io"},
        {"name": "AWS_COGNITO_USER_POOL_ID", "value": ""},
        {"name": "AWS_COGNITO_USER_POOL_CLIENT_ID", "value": ""},
        {"name": "FRONTEND_URL", "value": ""},
        {"name": "BACKEND_URL", "value": ""},
        {"name": "AWS_DEFAULT_REGION", "value": ""}
      ],
      "secrets": [
        {"name": "AWS_ACCESS_KEY_ID"    , "valueFrom": "arn:aws:ssm:AWS_REGION:AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/AWS_ACCESS_KEY_ID"},
        {"name": "AWS_SECRET_ACCESS_KEY", "valueFrom": "arn:aws:ssm:AWS_REGION:AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/AWS_SECRET_ACCESS_KEY"},
        {"name": "CONNECTION_URL"       , "valueFrom": "arn:aws:ssm:AWS_REGION:AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/CONNECTION_URL" },
        {"name": "ROLLBAR_ACCESS_TOKEN" , "valueFrom": "arn:aws:ssm:AWS_REGION:AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/ROLLBAR_ACCESS_TOKEN" },
        {"name": "OTEL_EXPORTER_OTLP_HEADERS" , "valueFrom": "arn:aws:ssm:AWS_REGION:AWS_ACCOUNT_ID:parameter/cruddur/backend-flask/OTEL_EXPORTER_OTLP_HEADERS" }
        
      ]
    }
  ]
}
```

`frontend-react.json`

```json
{
  "family": "frontend-react-js",
  "executionRoleArn": "arn:aws:iam::AWS_ACCOUNT_ID:role/CruddurServiceExecutionRole",
  "taskRoleArn": "arn:aws:iam::AWS_ACCOUNT_ID:role/CruddurTaskRole",
  "networkMode": "awsvpc",
  "containerDefinitions": [
    {
      "name": "frontend-react-js",
      "image": "BACKEND_FLASK_IMAGE_URL",
      "cpu": 256,
      "memory": 256,
      "essential": true,
      "portMappings": [
        {
          "name": "frontend-react-js",
          "containerPort": 3000,
          "protocol": "tcp", 
          "appProtocol": "http"
        }
      ],

      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
            "awslogs-group": "cruddur",
            "awslogs-region": "ca-central-1",
            "awslogs-stream-prefix": "frontend-react"
        }
      }
    }
  ]
}
```

### Register Task Defintion

```sh
aws ecs register-task-definition --cli-input-json file://aws/task-defintions/backend-flask.json
```


```sh
aws ecs register-task-definition --cli-input-json file://aws/task-defintions/frontend-react-js.json
```

### Create Security Group


```sh
export CRUD_SERVICE_SG=$(aws ec2 create-security-group \
  --group-name "crud-srv-sg" \
  --description "Security group for Cruddur services on ECS" \
  --vpc-id $DEFAULT_VPC_ID \
  --query "GroupId" --output text)
echo $CRUD_SERVICE_SG
```


```sh
aws ec2 authorize-security-group-ingress \
  --group-id $CRUD_SERVICE_SG \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0
```


> if we need to get the sg group id  again
```sh
export CRUD_SERVICE_SG=$(aws ec2 describe-security-groups \
  --filters Name=group-name,Values=crud-srv-sg \
  --query 'SecurityGroups[*].GroupId' \
  --output text)
```

#### Update RDS SG to allow access for the last security group

```sh
aws ec2 authorize-security-group-ingress \
  --group-id $DB_SG_ID \
  --protocol tcp \
  --port 5432 \
  --source-group $CRUD_SERVICE_SG \
  --tag-specifications 'ResourceType=security-group,Tags=[{Key=Name,Value=BACKENDFLASK}]'
```

### Create Services

```sh
aws ecs create-service --cli-input-json file://aws/json/backend-flask-serv.json
```

```sh
aws ecs create-service --cli-input-json file://aws/json/frontend-react-js-serv.json
```

> Auto Assign is not supported by EC2 launch type for services

This is for when we are uing a NetworkMode of awsvpc
> --network-configuration "awsvpcConfiguration={subnets=[$DEFAULT_SUBNET_IDS],securityGroups=[$SERVICE_CRUD_SG],assignPublicIp=ENABLED}"

https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking.html

### Test Service

Use sessions manager to connect to the EC2 instance.

#### Test RDS Connection

Shell into the backend flask container and run the `./bin/db/test` script to ensure we have a database connection


#### Test Flask App is running

`./bin/flask/health-check`

Check our forwarding ports for the container

```sh
docker port <CONTAINER_ID>
```

> docker run --rm --link <container_name_or_id>:<alias> curlimages/curl curl <alias>:<port>/<endpoint>

```sh
docker run --rm --link d71eea0b8e93:flask -it curlimages/curl --get -H "Accept: application/json" -H "Content-Type: application/json" http://flask:4567/api/activities/home
```

#### Check endpoiint against Public IP 

```sh
docker run --rm -it curlimages/curl --get -H "Accept: application/json" -H "Content-Type: application/json" http://3.97.113.133/api/activities/home
```



## Not able to use Sessions Manager to get into cluster EC2 sintance

The instance can hang up for various reasons.
You need to reboot and it will force a restart after 5 minutes
So you will have to wait 5 minutes or after a timeout.

You have to use the AWS CLI. 
You can't use the AWS Console. it will not work as expected.

The console will only do a graceful shutdodwn
The CLI will do a forceful shutdown after a period of time if graceful shutdown fails.

```sh
aws ec2 reboot-instances --instance-ids i-0d15aef0618733b6d
```