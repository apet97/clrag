---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-script-running-pg-support-queries",
  "h1": "langsmith-script-running-pg-support-queries",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.440928",
  "sha256_raw": "7c5cdf79ed604b41798de497e64a9451a0138f654f96733758bd9bcc272d9a18"
}
---

# langsmith-script-running-pg-support-queries

> Source: https://docs.langchain.com/langsmith/script-running-pg-support-queries

pg_get_trace_counts_daily.sql
input file in the support_queries/postgres
directory.
Prerequisites
Ensure you have the following tools/items ready.- kubectl
- PostgreSQL client
-
PostgreSQL database connection:
- Host
- Port
- Username
- If using the bundled version, this is
postgres
- If using the bundled version, this is
- Password
- If using the bundled version, this is
postgres
- If using the bundled version, this is
- Database name
- If using the bundled version, this is
postgres
- If using the bundled version, this is
-
Connectivity to the PostgreSQL database from the machine you will be running the migration script on.
- If you are using the bundled version, you may need to port forward the postgresql service to your local machine.
- Run
kubectl port-forward svc/langsmith-postgres 5432:5432
to port forward the postgresql service to your local machine.
-
The script to run a support query
- You can download the script from here
Running the query script
Run the following command to run the desired query:--output path/to/file.csv
Export usage data
Exporting usage data requires running Helm chart version 0.11.4 or later.
Get customer information
You need to retrieve your customer information from the LangSmith API before running the export scripts. This information is required as input for the export scripts.customer_id
and customer_name
from this response to use as input for the export scripts.
Process the API response with jq
You can use jq to parse the JSON response and set bash variables for use in your scripts:jq
, run these commands to set the environment variables based on the curl output:
Initial export
These scripts export usage data to a CSV for reporting to LangChain. They additionally track the export by assigning a backfill ID and timestamp. To export LangSmith trace usage:Status update
These scripts update the status of usage events in your installation to reflect that the events have been successfully processed by LangChain. The scripts require passing in the correspondingbackfill_id
, which will be confirmed by your LangChain rep.
To update LangSmith trace usage: