---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-script-generate-clickhouse-stats",
  "h1": "langsmith-script-generate-clickhouse-stats",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.448683",
  "sha256_raw": "3ab9b6b045e0960f33726ea6a103aba6ddb2dbbf2feb30d3029f489cd6b3a230"
}
---

# langsmith-script-generate-clickhouse-stats

> Source: https://docs.langchain.com/langsmith/script-generate-clickhouse-stats

Skip to main content
As part of troubleshooting your self-hosted instance of LangSmith, the LangChain team may ask you to generate Clickhouse statistics that will help us understand memory and CPU consumption and connection concurrency.
This command will generate a CSV that can be shared with the LangChain team.
Prerequisites
Ensure you have the following tools/items ready.
kubectl
Clickhouse database credentials
Host
Port
Username
If using the bundled version, this is default
Password
If using the bundled version, this is password
Database name
If using the bundled version, this is default
Connectivity to the Clickhouse database from the machine you will be running the get_clickhouse_stats
script on.
If you are using the bundled version, you may need to port forward the clickhouse service to your local machine.
Run kubectl port-forward svc/langsmith-clickhouse 8123:8123
to port forward the clickhouse service to your local machine.
The script to generate ClickHouse stats
You can download the script from here
Running the clickhouse stats generation script
Run the following command to run the stats generation script:
For example, if you are using the bundled version with port-forwarding, the command would look like:
and after running this command you should see a file, clickhouse_stats.csv, has been created with Clickhouse statistics.