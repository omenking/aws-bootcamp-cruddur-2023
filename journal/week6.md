# Week 6 — Deploying Containers

## Install Docker Compose CLI
https://docs.docker.com/cloud/ecs-integration/#install-the-docker-compose-cli-on-linux

```gitpod.yml
curl -L https://raw.githubusercontent.com/docker/compose-cli/main/scripts/install/install_linux.sh | sh
```

## Login to ECR

```
aws ecr get-login-password --region ca-central-1 | sudo docker login --username AWS --password-stdin 387543059434.dkr.ecr.ca-central-1.amazonaws.com
```

## Create ECR repositories

```
aws ecr create-repository \
  --repository-name cruddur/backend-flask

aws ecr create-repository \
  --repository-name cruddur/frontend-react-js

aws ecr create-repository \
  --repository-name cruddur/xray-daemon
```

387543059434.dkr.ecr.ca-central-1.amazonaws.com/cruddur/frontend-react-js
387543059434.dkr.ecr.ca-central-1.amazonaws.com/cruddur/backend-flask
387543059434.dkr.ecr.ca-central-1.amazonaws.com/cruddur/xray-daemon

## Tag & push images

```
docker tag f90df27438bd 387543059434.dkr.ecr.ca-central-1.amazonaws.com/cruddur/frontend-react-js
docker tag 3bf638f11bce 387543059434.dkr.ecr.ca-central-1.amazonaws.com/cruddur/backend-flask
docker tag 454a03e38abd 387543059434.dkr.ecr.ca-central-1.amazonaws.com/cruddur/xray-daemon

docker push 387543059434.dkr.ecr.ca-central-1.amazonaws.com/cruddur/frontend-react-js
docker push 387543059434.dkr.ecr.ca-central-1.amazonaws.com/cruddur/backend-flask
docker push 387543059434.dkr.ecr.ca-central-1.amazonaws.com/cruddur/xray-daemon
```

## Add Vars to docker-compose

```
x-aws-vpc: vpc-0ab94d84a784b412e
x-aws-cluster: arn:aws:ecs:ca-central-1:387543059434:cluster/bayko-test
```


## Create and enable docker context

```
sudo docker context create cruddur
sudo docker context use cruddur
```

## Deploy to ECS

```
sudo docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```







