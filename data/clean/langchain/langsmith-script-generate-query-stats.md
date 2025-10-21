---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-script-generate-query-stats",
  "h1": "langsmith-script-generate-query-stats",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.489593",
  "sha256_raw": "cc7c04c3057e5cd93080f5872337952c418c96d653bc05c9f9ee9ec8dce4b557"
}
---

# langsmith-script-generate-query-stats

> Source: https://docs.langchain.com/langsmith/script-generate-query-stats

Skip to main content
As part of troubleshooting your self-hosted instance of LangSmith, the LangChain team may ask you to generate LangSmith query statistics that will help us understand the performance of various queries that drive the LangSmith product experience.
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
Connectivity to the Clickhouse database from the machine you will be running the get_query_stats
script on.
If you are using the bundled version, you may need to port forward the clickhouse service to your local machine.
Run kubectl port-forward svc/langsmith-clickhouse 8123:8123
to port forward the clickhouse service to your local machine.
The script to generate query stats
You can download the script from here
Running the query stats generation script
Run the following command to run the stats generation script:
For example, if you are using the bundled version with port-forwarding, the command would look like:
and after running this command you should see a file, query_stats.csv, has been created with LangSmith query statistics.