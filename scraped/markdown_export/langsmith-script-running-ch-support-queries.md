# langsmith-script-running-ch-support-queries

> Source: https://docs.langchain.com/langsmith/script-running-ch-support-queries

This Helm repository contains queries to produce output that the LangSmith UI does not currently support directly (e.g. obtaining query exception logs from Clickhouse).This command takes a clickhouse connection string that contains an embedded name and password (which can be passed in from a call to a secrets manager) and executes a query from an input file. In the example below, we are using the ch_get_query_exceptions.sql input file in the support_queries/clickhouse directory.
Run the following command to run the desired query:
Copy
sh run_support_query_ch.sh <clickhouse_url> --input path/to/query.sql
For example, if you are using the bundled version with port-forwarding, the command might look like:
Copy
sh run_support_query_ch.sh "clickhouse://default:password@localhost:8123/default" --input support_queries/clickhouse/ch_get_query_exceptions.sql
which will output query logs for all queries that have thrown exceptions in Clickhouse in the last 7 days. To extract this to a file add the flag --output path/to/file.csv