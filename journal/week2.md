# Week 2 — Distributed Tracing
<br />

# New topics learned

 - [Observability vs Monitoring vs Telemetry: Understanding the Key Differences](https://cribl.io/blog/observability-vs-monitoring-vs-telemetry/)

   ![Monitoring vs Observability](https://i.ytimg.com/vi/31mHDchkXKQ/maxresdefault.jpg)
   
   
# Tasks completed
 - Instrument the backend app with Honeycomb Open Telemetry (OTEL)

   ![Honeycomb 1](Week2/Honeycomb%201.png) 
   
   ![Honeycomb 1](Week2/Honeycomb%202.png) 

 - CloudWatch Logs
 
   Add the following package to backend-flask/requirements.txt
   ```
    watchtower
   ```
   ![CloudWatch Logs](Week2/CloudWatch%20Logs.png) 

 - Cloud Watch Log groups

   ![CloudWatch Log groups 1](Week2/CloudWatch%20Log%20groups%201.png)
   
   ![CloudWatch Log groups 2](Week2/CloudWatch%20Log%20groups%202.png)
   
 - Implement AWS Xray 

   Add the following package to backend-flask/requirements.txt
   ```
    aws-xray-sdk
   ```
   
   Edit docker-compose.yml and Add:
   
   ```
   version: "3.8"
   services:
       backend-flask:
           environment:
               ...
               AWS_XRAY_URL: "*4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}*"
               AWS_XRAY_DAEMON_ADDRESS: "xray-daemon:2000"

       ...
       xray-daemon:
           image: "amazon/aws-xray-daemon"
           environment:
               AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
               AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
               AWS_REGION: "us-east-1"
           command:
               - "xray -o -b xray-daemon:2000"
           ports:
               - 2000:2000/udp
   ```
   
   Then I ran the following command to group Xray traces:
   ```
   $ aws xray create-group \
   --group-name "Cruddur" \
   --filter-expression "service(\"backend-flask\")"
   ```
   Created a sampling rule for Xray service ![aws/json/xray.json](https://github.com/Peter2220/aws-bootcamp-cruddur-2023/blob/main/aws/json/xray.json)
  
   ```
   {
   "SamplingRule": {
       "RuleName": "Cruddur",
       "ResourceARN": "*",
       "Priority": 9000,
       "FixedRate": 0.1,
       "ReservoirSize": 5,
       "ServiceName": "backend-flask",
       "ServiceType": "*",
       "Host": "*",
       "HTTPMethod": "*",
       "URLPath": "*",
       "Version": 1
       }
   }
   ```
   
   Run the following command in the terminal
   ```
   $ aws xray create-sampling-rule --cli-input-json file://aws/json/xray.json
   ```
   
   Add the following to ![/backend-flask/app.py](https://github.com/Peter2220/aws-bootcamp-cruddur-2023/blob/main/backend-flask/app.py)
   ```
   ...
   ...

   # X_RAY
   from aws_xray_sdk.core import xray_recorder
   from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

   xray_url = os.getenv("AWS_XRAY_URL")
   #xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)
   xray_recorder.configure(service='backend-flask') # To make sure that all traces can be grouped under the created Cruudr group 

   ......
   ......

   app = Flask(__name__)

   #XRAY
   XRayMiddleware(app, xray_recorder)
   ```
   
 - Xray Traces in the AWS Console

   ![Xray Traces](Week2/Xray%20Traces.png) 
   
   ![Xray AWS CLI](Week2/Xray%20AWS%20CLI.png) 
 
 - Implement Rollbar
 
   Add the following package to backend-flask/requirements.txt
   ```
    blinker
    rollbar
   ```
   ![Fix ROLLBAR_ACCESS_TOKEN error](Week2/Fix%20ROLLBAR_ACCESS_TOKEN%20error.png) 


 - Important resources<br />
   [AWS X-Ray daemon (Application Instrumentation = Produce logs, traces)](https://docs.aws.amazon.com/xray/latest/devguide/xray-daemon.html)<br />
   [aws-xray-sdk-python](https://github.com/aws/aws-xray-sdk-python)<br />
   [OpenTelemetry for Python](https://docs.honeycomb.io/getting-data-in/opentelemetry/python/)<br />
   [What Honeycomb.io team is this? Test Honeycomb API Key](http://honeycomb-whoami.glitch.me/)<br />
