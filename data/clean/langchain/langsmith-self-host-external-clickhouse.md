---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-self-host-external-clickhouse",
  "h1": "langsmith-self-host-external-clickhouse",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.443669",
  "sha256_raw": "fef901ad6d9fc267fb08f30220b6cf8ddea96762a4b16d33fc762cb9bc5c2348"
}
---

# langsmith-self-host-external-clickhouse

> Source: https://docs.langchain.com/langsmith/self-host-external-clickhouse

- LangSmith-managed ClickHouse
- Provision a ClickHouse Cloud either directly or through a cloud provider marketplace:
- On a VM in your cloud provider
Using the first two options (LangSmith-managed ClickHouse or ClickHouse Cloud) will provision a Clickhouse service OUTSIDE of your VPC. However, both options support private endpoints, meaning that you can direct traffic to the ClickHouse service without exposing it to the public internet (eg via AWS PrivateLink, or GCP Private Service Connect).Additionally, sensitive information can be configured to be not stored in Clickhouse. Please reach out to support@langchain.dev for more information.
Requirements
- A provisioned ClickHouse instance that your LangSmith application will have network access to (see above for options).
- A user with admin access to the ClickHouse database. This user will be used to create the necessary tables, indexes, and views.
- We support both standalone ClickHouse and externally managed clustered deployments. For clustered deployments, ensure all nodes are running the same version. Note that clustered setups are not supported with bundled ClickHouse installations.
- We only support ClickHouse versions >= 23.9. Use of ClickHouse versions >= 24.2 requires LangSmith v0.6 or later.
- We rely on a few configuration parameters to be set on your ClickHouse instance. These are detailed below:
Our system has been tuned to work with the above configuration parameters. Changing these parameters may result in unexpected behavior.
HA Replicated Clickhouse Cluster
By default, the setup process above will only work with a single node Clickhouse cluster.
- You need to have a Clickhouse cluster that is setup with Keeper or Zookeeper for data replication and the appropriate settings. See Clickhouse Replication Setup Docs.
- You need to set the cluster setting in the LangSmith Configuration section, specifically the
cluster
settings to match your Clickhouse Cluster name. This will use theReplicated
table engines when running the Clickhouse migrations. - If in addition to HA, you would like to load balance among the Clickhouse nodes (to distribute reads or writes), we suggest using a load balancer or DNS load balancing to round robin among your Clickhouse servers.
- Note: You will need to enable your
cluster
setting before launching LangSmith for the first time and running the Clickhouse migrations. This is a requirement since the table engine will need to be created as aReplicated
table engine vs the non replicated engine type.
cluster
enabled, the migration will create the Replicated
table engine flavor. This means that data will be replicated among the servers in the cluster. This is a master-master setup where any server can process reads, writes, or merges.
LangSmith-managed ClickHouse
- If using LangSmith-managed ClickHouse, you will need to set up a VPC peering connection between the LangSmith VPC and the ClickHouse VPC. Please reach out to support@langchain.dev for more information.
- You will also need to set up Blob Storage. You can read more about Blob Storage in the Blob Storage documentation.
ClickHouse installations managed by LangSmith use a SharedMerge engine, which automatically clusters them and separates compute from storage.
Parameters
You will need to provide several parameters to your LangSmith installation to configure an external ClickHouse database. These parameters include:- Host: The hostname or IP address of the ClickHouse database
- HTTP Port: The port that the ClickHouse database listens on for HTTP connections
- Native Port: The port that the ClickHouse database listens on for native connections
- Database: The name of the ClickHouse database that LangSmith should use
- Username: The username to use to connect to the ClickHouse database
- Password: The password to use to connect to the ClickHouse database
- Cluster (Optional): The name of the ClickHouse cluster if using an external Clickhouse cluster. When set, LangSmith will run migrations on the cluster and replicate data across instances.
Important considerations for clustered deployments:
- Clustered setups must be configured on a fresh schema - existing standalone ClickHouse instances cannot be converted to clustered mode.
- Clustering is only supported with externally managed ClickHouse deployments. It is not compatible with bundled ClickHouse installations as these do not include required ZooKeeper configurations.
- When using a clustered deployment, LangSmith will automatically:
- Run database migrations across all nodes in the cluster
- Configure tables for data replication across the cluster
Configuration
With these parameters in hand, you can configure your LangSmith instance to use the provisioned ClickHouse database. You can do this by modifying theconfig.yaml
file for your LangSmith Helm Chart installation or the .env
file for your Docker installation.