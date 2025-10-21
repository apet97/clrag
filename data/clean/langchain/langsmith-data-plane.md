---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-data-plane",
  "h1": "langsmith-data-plane",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.481873",
  "sha256_raw": "50948db7c43654f302238b61203376aa16f9dc88c981122173b3e2cba71f84bf"
}
---

# langsmith-data-plane

> Source: https://docs.langchain.com/langsmith/data-plane

Server infrastructure
In addition to the LangGraph Server itself, the following infrastructure components for each server are also included in the broad definition of “data plane”:- PostgreSQL: persistence layer for user, run, and memory data.
- Redis: communication and ephemeral metadata for workers.
- Secrets store: secure management of environment secrets.
- Autoscalers: scale server containers based on load.
”Listener” application
The data plane “listener” application periodically calls control plane APIs to:- Determine if new deployments should be created.
- Determine if existing deployments should be updated (i.e. new revisions).
- Determine if existing deployments should be deleted.
PostgreSQL
PostgreSQL is the persistence layer for all user, run, and long-term memory data in a LangGraph Server. This stores both checkpoints (see more info here), server resources (threads, runs, assistants and crons), as well as items saved in the long-term memory store (see more info here).Redis
Redis is used in each LangGraph Server as a way for server and queue workers to communicate, and to store ephemeral metadata. No user or run data is stored in Redis.Communication
All runs in a LangGraph Server are executed by a pool of background workers that are part of each deployment. In order to enable some features for those runs (such as cancellation and output streaming) we need a channel for two-way communication between the server and the worker handling a particular run. We use Redis to organize that communication.- A Redis list is used as a mechanism to wake up a worker as soon as a new run is created. Only a sentinel value is stored in this list, no actual run information. The run information is then retrieved from PostgreSQL by the worker.
- A combination of a Redis string and Redis PubSub channel is used for the server to communicate a run cancellation request to the appropriate worker.
- A Redis PubSub channel is used by the worker to broadcast streaming output from an agent while the run is being handled. Any open
/stream
request in the server will subscribe to that channel and forward any events to the response as they arrive. No events are stored in Redis at any time.
Ephemeral metadata
Runs in a LangGraph Server may be retried for specific failures (currently only for transient PostgreSQL errors encountered during the run). In order to limit the number of retries (currently limited to 3 attempts per run) we record the attempt number in a Redis string when it is picked up. This contains no run-specific info other than its ID, and expires after a short delay.Data plane features
This section describes various features of the data plane.Data region
Deployments can be created in 2 data regions: US and EU The data region for a deployment is implied by the data region of the LangSmith organization where the deployment is created. Deployments and the underlying database for the deployments cannot be migrated between data regions.Autoscaling
Production
type deployments automatically scale up to 10 containers. Scaling is based on 3 metrics:
- CPU utilization
- Memory utilization
- Number of pending (in progress) runs
Static IP addresses
All traffic from deployments created after January 6th 2025 will come through a NAT gateway. This NAT gateway will have several static IP addresses depending on the data region. Refer to the table below for the list of static IP addresses:| US | EU |
|---|---|
| 35.197.29.146 | 34.13.192.67 |
| 34.145.102.123 | 34.147.105.64 |
| 34.169.45.153 | 34.90.22.166 |
| 34.82.222.17 | 34.147.36.213 |
| 35.227.171.135 | 34.32.137.113 |
| 34.169.88.30 | 34.91.238.184 |
| 34.19.93.202 | 35.204.101.241 |
| 34.19.34.50 | 35.204.48.32 |
| 34.59.244.194 | |
| 34.9.99.224 | |
| 34.68.27.146 | |
| 34.41.178.137 | |
| 34.123.151.210 | |
| 34.135.61.140 | |
| 34.121.166.52 | |
| 34.31.121.70 |
Custom PostgreSQL
A custom PostgreSQL instance can be used instead of the one automatically created by the control plane. Specify thePOSTGRES_URI_CUSTOM
environment variable to use a custom PostgreSQL instance.
Multiple deployments can share the same PostgreSQL instance. For example, for Deployment A
, POSTGRES_URI_CUSTOM
can be set to postgres://<user>:<password>@/<database_name_1>?host=<hostname_1>
and for Deployment B
, POSTGRES_URI_CUSTOM
can be set to postgres://<user>:<password>@/<database_name_2>?host=<hostname_1>
. <database_name_1>
and database_name_2
are different databases within the same instance, but <hostname_1>
is shared. The same database cannot be used for separate deployments.
Custom Redis
A custom Redis instance can be used instead of the one automatically created by the control plane. Specify the REDIS_URI_CUSTOM environment variable to use a custom Redis instance. Multiple deployments can share the same Redis instance. For example, forDeployment A
, REDIS_URI_CUSTOM
can be set to redis://<hostname_1>:<port>/1
and for Deployment B
, REDIS_URI_CUSTOM
can be set to redis://<hostname_1>:<port>/2
. 1
and 2
are different database numbers within the same instance, but <hostname_1>
is shared. The same database number cannot be used for separate deployments.
LangSmith tracing
LangGraph Server is automatically configured to send traces to LangSmith. See the table below for details with respect to each deployment option.| Cloud | Hybrid | Self-Hosted |
|---|---|---|
| Required Trace to LangSmith SaaS. | Optional Disable tracing or trace to LangSmith SaaS. | Optional Disable tracing, trace to LangSmith SaaS, or trace to Self-Hosted LangSmith. |
Telemetry
LangGraph Server is automatically configured to report telemetry metadata for billing purposes. See the table below for details with respect to each deployment option.| Cloud | Hybrid | Self-Hosted |
|---|---|---|
| Telemetry sent to LangSmith SaaS. | Telemetry sent to LangSmith SaaS. | Self-reported usage (audit) for air-gapped license key. Telemetry sent to LangSmith SaaS for LangSmith License Key. |
Licensing
LangGraph Server is automatically configured to perform license key validation. See the table below for details with respect to each deployment option.| Cloud | Hybrid | Self-Hosted |
|---|---|---|
| LangSmith API Key validated against LangSmith SaaS. | LangSmith API Key validated against LangSmith SaaS. | Air-gapped license key or Platform License Key validated against LangSmith SaaS. |