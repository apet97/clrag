# langsmith-self-host-scale

> Source: https://docs.langchain.com/langsmith/self-host-scale

Summary
The table below provides an overview comparing different LangSmith configurations for various load patterns (reads / writes):| Low / low | Low / high | High / low | Medium / medium | High / high | |
|---|---|---|---|---|---|
| 5 | 5 | 50 | 20 | 50 | |
| 10 | 1000 | 10 | 100 | 1000 | |
| Frontend replicas | 1 (default) | 4 | 2 | 2 | 4 |
| Platform backend replicas | 3 (default) | 20 | 3 (default) | 3 (default) | 20 |
| Queue replicas | 3 (default) | 160 | 6 | 10 | 160 |
| Backend replicas | 2 (default) | 5 | 40 | 16 | 50 |
| Redis resources | 8 Gi (default) | 200 Gi external | 8 Gi (default) | 13Gi external | 200 Gi external |
| ClickHouse resources | 4 CPU 16 Gi (default) | 10 CPU 32Gi memory | 8 CPU 16 Gi per replica | 16 CPU 24Gi memory | 14 CPU 24 Gi per replica |
| ClickHouse setup | Single instance | Single instance | 3-node | Single instance | 3-node |
| 2 CPU 8 GB memory 10GB storage (external) | 2 CPU 8 GB memory 10GB storage (external) | 2 CPU 8 GB memory 10GB storage (external) | 2 CPU 8 GB memory 10GB storage (external) | 2 CPU 8 GB memory 10GB storage (external) | |
| Blob storage | Disabled | Enabled | Enabled | Enabled | Enabled |
values.yaml
snippet for you to start with for your self-hosted LangSmith instance.
Trace ingestion (write path)
Common usage that put load on the write path:- Ingesting traces via the Python or JavaScript LangSmith SDK
- Ingesting traces via the
@traceable
wrapper - Submitting traces via the
/runs/multipart
endpoint
- Platform backend service: Receives initial request to ingest traces and places traces on a Redis queue
- Redis cache: Used to queue traces that need to be persisted
- Queue service: Persists traces for querying
- ClickHouse: Persistent storage used for traces
- Give ClickHouse more resources (CPU and memory) if it is approaching resource limits.
- Increase the number of platform-backend pods if ingest requests are taking long to respond.
- Increase queue service pod replicas if traces are not being processed from Redis fast enough.
- Use a larger Redis cache if you notice that the current Redis instance is reaching resource limits. This could also be a reason why ingest requests take a long time.
Trace querying (read path)
Common usage that puts load on the read path:- Users on the frontend looking at tracing projects or individual traces
- Scripts used to query for trace info
- Hitting either the
/runs/query
or/runs/<run-id>
api endpoints
- Backend service: Receives the request and submits a query to ClickHouse to then respond to the request
- ClickHouse: Persistent storage for traces. This is the main database that is queried when requesting trace info.
- Increase the number of backend service pods. This would be most impactful if backend service pods are reaching 1 core CPU usage.
- Give ClickHouse more resources (CPU or Memory). ClickHouse can be very resource intensive, but it should lead to better performance.
- Move to a replicated ClickHouse cluster. Adding replicas of ClickHouse helps with read performance, but we recommend staying below 5 replicas (start with 3).
Example LangSmith configurations for scale
Below we provide some example LangSmith configurations based on expected read and write loads. For read load (trace querying):- Low means roughly 5 users looking at traces at a time (about 10 requests per second)
- Medium means roughly 20 users looking at traces at a time (about 40 requests per second)
- High means roughly 50 users looking at traces at a time (about 100 requests per second)
- Low means up to 10 traces submitted per second
- Medium means up to 100 traces submitted per second
- High means up to 1000 traces submitted per second
The exact optimal configuration depends on your usage and trace payloads. Use the examples below in combination with the information above and your specific usage to update your LangSmith configuration as you see fit. If you have any questions, please reach out to the LangChain team.
/runs/query
or /runs/<run-id>
endpoints frequently.
For this, we strongly recommend setting up a replicated ClickHouse cluster to enable high read scale at low latency. See our external ClickHouse doc for more guidance on how to setup a replicated ClickHouse cluster. For this load pattern, we recommend using a 3 node replicated setup, where each replica in the cluster should have resource requests of 8+ cores and 16+ GB memory, and resource limit of 12 cores and 32 GB memory.
For this, we recommend a configuration like this:
You have a very high rate of trace ingestion (approaching 1000 traces submitted per second) and also have many users querying traces on the frontend (over 50 users) and/or scripts that are consistently making requests to
/runs/query
or /runs/<run-id>
endpoints.
For this, we very strongly recommend setting up a replicated ClickHouse cluster to prevent degraded read performance at high write scale. See our external ClickHouse doc for more guidance on how to set up a replicated ClickHouse cluster. For this load pattern, we recommend using a 3 node replicated setup, where each replica in the cluster should have resource requests of 14+ cores and 24+ GB memory, and resource limit of 20 cores and 48 GB memory. We also recommend that each node/instance of ClickHouse has 600 Gi of volume storage for each day of TTL that you enable (as per the configuration below).
Overall, we recommend a configuration like this:
Ensure that the Kubernetes cluster is configured with sufficient resources to scale to the recommended size. After deployment, all of the pods in the Kubernetes cluster should be in a
Running
state. Pods stuck in Pending
may indicate that you are reaching node pool limits or need larger nodes.Also, ensure that any ingress controller deployed on the cluster is able to handle the desired load to prevent bottlenecks.