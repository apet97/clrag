# langsmith-self-host-external-redis

> Source: https://docs.langchain.com/langsmith/self-host-external-redis

Requirements
- A provisioned Redis instance that your LangSmith instance will have network access to. We recommend using a managed Redis service like:
- Note: We only officially support Redis versions >= 5.
- We do not support Redis Cluster.
- By default, we recommend an instance with at least 2 vCPUs and 8GB of memory. However, the actual requirements will depend on your tracing workload. We recommend monitoring your Redis instance and scaling up as needed.
Certain tiers of managed Redis services may use Redis Cluster under the hood, but you can point to a single node in the cluster. For example on Azure Cache for Redis, the
Premium
tier and above use Redis Cluster, so you will need to use a lower tier.Connection String
We useredis-py
to connect to Redis. This library supports a variety of connection strings. You can find more information on the connection string format here.
You will need to assemble the connection string for your Redis instance. This connection string should include the following information:
- Host
- Database
- Port
- URL params
rediss://
prefix. An example connection string with SSL might look like:
Configuration
With your connection string in hand, you can configure your LangSmith instance to use an external Redis instance. You can do this by modifying thevalues
file for your LangSmith Helm Chart installation or the .env
file for your Docker installation.