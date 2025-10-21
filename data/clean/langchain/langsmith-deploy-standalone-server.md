---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-deploy-standalone-server",
  "h1": "langsmith-deploy-standalone-server",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.433010",
  "sha256_raw": "e81f7123de77227a95fff6d16f17a17f60881f94fac136544e1f7c74c2e4522d"
}
---

# langsmith-deploy-standalone-server

> Source: https://docs.langchain.com/langsmith/deploy-standalone-server

This is the setup page for deploying LangGraph Servers directly without the LangSmith platform.Review the self-hosted options to understand:
- Standalone Server: What this guide covers (no UI, just servers).
- LangSmith: For the full LangSmith platform with UI.
- LangSmith with deployment: For UI-based deployment management.
Prerequisites
- Use the LangGraph CLI to test your application locally.
-
Use the LangGraph CLI to build a Docker image (i.e.
langgraph build
). - The following environment variables are needed for a data plane deployment.
-
REDIS_URI
: Connection details to a Redis instance. Redis will be used as a pub-sub broker to enable streaming real time output from background runs. The value ofREDIS_URI
must be a valid Redis connection URI.Shared Redis Instance Multiple self-hosted deployments can share the same Redis instance. For example, forDeployment A
,REDIS_URI
can be set toredis://<hostname_1>:<port>/1
and forDeployment B
,REDIS_URI
can be set toredis://<hostname_1>:<port>/2
.1
and2
are different database numbers within the same instance, but<hostname_1>
is shared. The same database number cannot be used for separate deployments. -
DATABASE_URI
: Postgres connection details. Postgres will be used to store assistants, threads, runs, persist thread state and long term memory, and to manage the state of the background task queue with ‘exactly once’ semantics. The value ofDATABASE_URI
must be a valid Postgres connection URI.Shared Postgres Instance Multiple self-hosted deployments can share the same Postgres instance. For example, forDeployment A
,DATABASE_URI
can be set topostgres://<user>:<password>@/<database_name_1>?host=<hostname_1>
and forDeployment B
,DATABASE_URI
can be set topostgres://<user>:<password>@/<database_name_2>?host=<hostname_1>
.<database_name_1>
anddatabase_name_2
are different databases within the same instance, but<hostname_1>
is shared. The same database cannot be used for separate deployments. -
LANGSMITH_API_KEY
: LangSmith API key. -
LANGGRAPH_CLOUD_LICENSE_KEY
: LangSmith license key. This will be used to authenticate ONCE at server start up. -
LANGSMITH_ENDPOINT
: To send traces to a self-hosted LangSmith instance, setLANGSMITH_ENDPOINT
to the hostname of the self-hosted LangSmith instance. -
Egress to
https://beacon.langchain.com
from your network. This is required for license verification and usage reporting if not running in air-gapped mode. See the Egress documentation for more details.
Kubernetes
Use this Helm chart to deploy a LangGraph Server to a Kubernetes cluster.Docker
Run the followingdocker
command:
- You need to replace
my-image
with the name of the image you built in the prerequisite steps (fromlanggraph build
)
REDIS_URI
, DATABASE_URI
, and LANGSMITH_API_KEY
.- If your application requires additional environment variables, you can pass them in a similar way.
Docker Compose
Docker Compose YAML file:docker compose up
with this Docker Compose file in the same folder.
This will launch a LangGraph Server on port 8123
(if you want to change this, you can change this by changing the ports in the langgraph-api
volume). You can test if the application is healthy by running: