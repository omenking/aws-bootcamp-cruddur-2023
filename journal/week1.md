# Week 1 — App Containerization
<br />

# New topics learned
 - Vulnerability Scanning Tools (Snyk)
 - Container Security Components include:-
     - Docker & Host Configuration
     - Securing Images
     - Secret Management
     - Application Security
     - Data Security
     - Monitoring Containers
     - Compliance Framework
 - Follow Security Best Practices [TrendMicro](https://www.trendmicro.com/en_us/devops/22/b/container-security-best-practices.html)
# Tasks completed
 -  First time using Snyk to scan for vulnerabilities
 
   ![Docker Snyk](Week1/Docker%20Snyk.png) 
   
 -  Snyk extension on Docker Desktop

   ![Snyk Docker Desktop Example](Week1/Snyk%20Docker%20Desktop%20Example.png)
   
 -  Vulnerabilities report (aws-bootcamp-cruddur-2023)

   ![Snyk Report](Week1/Snyk%20Report.png)

 -  Critical Vulnerabilities Fixed (e.g., Upgrade node:16.18-alpine to FROM node:16.19.1-alpine)
 
   ![Fix Critical Vulnerabilities](Week1/Fix%20Critical%20Vulnerabilities.png) 

 -  Running Backend Locally
   <br />
   In cURL, we can use or pipe the json_pp to pretty print the JSON output.

   ```
   curl http://127.0.0.1:4567/api/activities/home | json_pp
   ```
   
   ![BackEnd App Running 1](Week1/BackEnd%20App%20Running%201.png)
   
   ![BackEnd App Running 2](Week1/BackEnd%20App%20Running%202.png)
   
 -  Test Frontend 

   ![FrontEnd Running](Week1/FrontEnd%20Running.png)
   
-  Backend and Frontend images uploaded to dockerhub 
   [Backend Link](https://hub.docker.com/r/rocky20/backend-flask), [Frontend Link](https://hub.docker.com/r/rocky20/frontend-react-js)

   ![Dockerhub](Week1/Dockerhub.png)
