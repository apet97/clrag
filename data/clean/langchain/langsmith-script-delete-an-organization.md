---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-script-delete-an-organization",
  "h1": "langsmith-script-delete-an-organization",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.442676",
  "sha256_raw": "5f7a263ea56f6ae7aec934475b22c9c0b451e12e89c204a5e4af7915838e8c67"
}
---

# langsmith-script-delete-an-organization

> Source: https://docs.langchain.com/langsmith/script-delete-an-organization

Skip to main content
The LangSmith UI does not currently support the deletion of an individual organization from a self-hosted instance of LangSmith. This, however, can be accomplished by directly removing all traces from all materialized views in ClickHouse (except the runs_history views) and the runs and feedbacks tables and then removing the Organization from the Postgres tenants table.
This command using the Organization ID as an argument.
Prerequisites
Ensure you have the following tools/items ready.
kubectl
PostgreSQL client
PostgreSQL database connection:
Host
Port
Username
If using the bundled version, this is postgres
Password
If using the bundled version, this is postgres
Database name
If using the bundled version, this is postgres
Clickhouse database credentials
Host
Port
Username
If using the bundled version, this is default
Password
If using the bundled version, this is password
Database name
If using the bundled version, this is default
Connectivity to the PostgreSQL database from the machine you will be running the migration script on.
If you are using the bundled version, you may need to port forward the postgresql service to your local machine.
Run kubectl port-forward svc/langsmith-postgres 5432:5432
to port forward the postgresql service to your local machine.
Connectivity to the Clickhouse database from the machine you will be running the migration script on.
If you are using the bundled version, you may need to port forward the clickhouse service to your local machine.
Run kubectl port-forward svc/langsmith-clickhouse 8123:8123
to port forward the clickhouse service to your local machine.
If you are using Clickhouse Cloud you will want to specify the —ssl flag and use port 8443
The script to delete an organization
You can download the script from here
Running the deletion script for a single organization
Run the following command to run the organization removal script:
For example, if you are using the bundled version with port-forwarding, the command would look like:
If you visit the LangSmith UI, you should now see organization is no longer present.