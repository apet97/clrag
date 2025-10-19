# langsmith-docker

> Source: https://docs.langchain.com/langsmith/docker

Self-hosting LangSmith is an add-on to the Enterprise Plan designed for our largest, most security-conscious customers. See our pricing page for more detail, and contact our sales team if you want to get a license key to trial LangSmith in your environment.
Note that Docker Compose is limited to local development environments only and does not extend support to container services such as AWS Elastic Container Service, Azure Container Instances, and Google Cloud Run.
Prerequisites
-
Ensure Docker is installed and running on your system. You can verify this by running:
If you don’t see any server information in the output, make sure Docker is installed correctly and launch the Docker daemon.
- Recommended: At least 4 vCPUs, 16GB Memory available on your machine.
- You may need to tune resource requests/limits for all of our different services based off of organization size/usage
- Disk Space: LangSmith can potentially require a lot of disk space. Ensure you have enough disk space available.
- Recommended: At least 4 vCPUs, 16GB Memory available on your machine.
-
LangSmith License Key
- You can get this from your LangChain representative. Contact our sales team for more information.
-
Api Key Salt
- This is a secret key that you can generate. It should be a random string of characters.
- You can generate this using the following command:
-
Egress to
https://beacon.langchain.com
(if not running in offline mode)- LangSmith requires egress to
https://beacon.langchain.com
for license verification and usage reporting. This is required for LangSmith to function properly. You can find more information on egress requirements in the Egress section.
- LangSmith requires egress to
-
Configuration
- There are several configuration options that you can set in the
.env
file. You can find more information on the available configuration options in the Configuration section.
- There are several configuration options that you can set in the
Running via Docker Compose
The following explains how to run the LangSmith using Docker Compose. This is the most flexible way to run LangSmith without Kubernetes. The default configuration for Docker Compose is intended for local testing only and not for instances where any services are exposed to the public internet. In production, we highly recommend using a secured Kubernetes environment.1. Fetch the LangSmith docker-compose.yml
file
You can find the docker-compose.yml
file and related files in the LangSmith SDK repository here: LangSmith Docker Compose File
Copy the docker-compose.yml
file and all files in that directory from the LangSmith SDK to your project directory.
- Ensure that you copy the
users.xml
file as well.
2. Configure environment variables
- Copy the
.env.example
file from the LangSmith SDK to your project directory and rename it to.env
. - Configure the appropriate values in the
.env
file. You can find the available configuration options in the Configuration section.
docker-compose.yml
file directly or export them in your terminal. We recommend setting them in the .env
file.
3. Start server
Start the LangSmith application by executing the following command in your terminal:Validate your deployment:
-
Curl the exposed port of the
cli-langchain-frontend-1
container: -
Visit the exposed port of the
cli-langchain-frontend-1
container on your browser The LangSmith UI should be visible/operational athttp://localhost:1980
Checking the logs
If, at any point, you want to check if the server is running and see the logs, runStopping the server
Using LangSmith
Now that LangSmith is running, you can start using it to trace your code. You can find more information on how to use self-hosted LangSmith in the self-hosted usage guide. Your LangSmith instance is now running but may not be fully setup yet. If you used one of the basic configs, you may have deployed a no-auth configuration. In this state, there is no authentication or concept of user accounts nor API keys and traces can be submitted directly without an API key so long as the hostname is passed to the LangChain tracer/LangSmith SDK. As a next step, it is strongly recommended you work with your infrastructure administrators to:- Setup DNS for your LangSmith instance to enable easier access
- Configure SSL to ensure in-transit encryption of traces submitted to LangSmith
- Configure LangSmith for oauth authentication or basic authentication to secure your LangSmith instance
- Secure access to your Docker environment to limit access to only the LangSmith frontend and API
- Connect LangSmith to secured Postgres and Redis instances