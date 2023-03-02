# Week 0 — Billing and Architecture
<br />

# New topics learned
 - The Open Group Architecture Framework (TOGAF)
 - AWS Well-Architected Tool


# Tasks completed
 - LucidChart (Logical Diagram): 
![Logical Diagram](Week0/Crudder%20Logical.png)
 - LucidChart (Napkin Diagram): To be added
 
   [Lucidchart Link](https://lucid.app/lucidchart/d435e356-e576-428c-8abd-39ae4522374a/edit?invitationId=inv_0e61e914-b561-49b1-8f42-1f8495406c28) **(contains both diagrams)**

 - Enable MFA

 - Install AWS CLI on Linux

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```
 - Configure AWS environment variables in gitpod (avoid hard-coding secrets)

```
gp env AWS_ACCESS_KEY_ID="="**********""
gp env AWS_SECRET_ACCESS_KEY="**********"
gp env AWS_DEFAULT_REGION="**-**-*"
gp env EMAIL_ADDRESS="Test@***.com"
```
 - Verify AWS configuration 

```
$ aws sts get-caller-identity
```
 - Create a budget alarm to monitor spending
 
  ![Create Budget](Week0/3.%20Create%20Budget.png) 

 - Create a Billing alarm 
 
  ![Billing Alarm](Week0/4.%20Billing%20Alarm.png) 
  
 - Subscribe to SNS Topic 

 ```
 aws sns subscribe \
    --topic-arn="arn:aws:sns:us-east-1:**********" \
    --protocol=email \
    --notification-endpoint=$EMAIL_ADDRESS
 ```
  ![Subscribe to SNS Topic](Week0/1.%20Subscribe%20to%20SNS%20Topic.png) 

  ![Confirm Topic](Week0/2.%20Confirm%20SNS%20Topic.png) 
  

