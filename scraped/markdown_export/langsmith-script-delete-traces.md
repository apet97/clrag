# langsmith-script-delete-traces

> Source: https://docs.langchain.com/langsmith/script-delete-traces

Skip to main content
The LangSmith UI does not currently support the deletion of an individual trace. This, however, can be accomplished by directly removing the trace from all materialized views in ClickHouse (except the runs_history views) and the runs and feedback table themselves.
This command can either be run using a trace ID as an argument or using a file that is a list of trace IDs.
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
Connectivity to the Clickhouse database from the machine you will be running the delete_trace_by_id
script on.
If you are using the bundled version, you may need to port forward the clickhouse service to your local machine.
Run kubectl port-forward svc/langsmith-clickhouse 8123:8123
to port forward the clickhouse service to your local machine.
The script to delete a trace
You can download the script from here
Running the deletion script for a single trace
Run the following command to run the trace deletion script using a single trace ID:
For example, if you are using the bundled version with port-forwarding, the command would look like:
If you visit the LangSmith UI, you should now see specified trace ID is no longer present nor reflected in stats.
Running the deletion script for a multiple traces from a file with one trace ID per line
Run the following command to run the trace deletion script using a list of trace IDs:
For example, if you are using the bundled version with port-forwarding, the command would look like:
If you visit the LangSmith UI, you should now see all the specified traces have been removed.