---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-script-delete-a-workspace",
  "h1": "langsmith-script-delete-a-workspace",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.481593",
  "sha256_raw": "ce935901cdb4764fd431f7dbf0e00acfc0df7dd62bb29f683b083876b1be3e55"
}
---

# langsmith-script-delete-a-workspace

> Source: https://docs.langchain.com/langsmith/script-delete-a-workspace

The LangSmith UI does not currently support the deletion of an individual workspace from an organization. This, however, can be accomplished by directly removing all traces from all materialized views in ClickHouse (except the runs_history views) and the runs and feedbacks tables and then removing the Workspace from the Postgres tenants table.
This command using the Workspace ID as an argument.
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
Clickhouse database credentials
- Host
- Port
- Username
- If using the bundled version, this is
default
- If using the bundled version, this is
- Password
- If using the bundled version, this is
password
- If using the bundled version, this is
- Database name
- If using the bundled version, this is
default
- If using the bundled version, this is
-
Connectivity to the PostgreSQL database from the machine you will be running the migration script on.
- If you are using the bundled version, you may need to port forward the postgresql service to your local machine.
- Run
kubectl port-forward svc/langsmith-postgres 5432:5432
to port forward the postgresql service to your local machine.
-
Connectivity to the Clickhouse database from the machine you will be running the migration script on.
- If you are using the bundled version, you may need to port forward the clickhouse service to your local machine.
- Run
kubectl port-forward svc/langsmith-clickhouse 8123:8123
to port forward the clickhouse service to your local machine.
- Run
- If you are using Clickhouse Cloud you will want to specify the —ssl flag and use port
8443
- If you are using the bundled version, you may need to port forward the clickhouse service to your local machine.
-
The script to delete a workspace
- You can download the script from here