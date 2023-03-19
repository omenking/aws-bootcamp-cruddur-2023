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
   
 - Implement AWS X-ray 

   Add the following package to backend-flask/requirements.txt
   ```
    aws-xray-sdk
   ```

 - X-ray Traces

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