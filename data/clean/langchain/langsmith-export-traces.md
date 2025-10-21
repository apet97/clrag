---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-export-traces",
  "h1": "langsmith-export-traces",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.433139",
  "sha256_raw": "e095d332a6483b5099cf488e7920d5fc60d458e9a7c291275fd93091bc58ca3c"
}
---

# langsmith-export-traces

> Source: https://docs.langchain.com/langsmith/export-traces

If you are looking to export a large volume of traces, we recommend that you use the Bulk Data Export functionality, as it will better handle large data volumes and will support automatic retries and parallelization across partitions.
list_runs
method in the SDK or /runs/query
endpoint in the API.
LangSmith stores traces in a simple format that is specified in the Run (span) data format.
Use filter arguments
For simple queries, you don’t have to rely on our query syntax. You can use the filter arguments specified in the filter arguments reference.PrerequisitesInitialize the client before running the below code snippets.
List all runs in a project
List LLM and Chat runs in the last 24 hours
List root runs in a project
Root runs are runs that have no parents. These are assigned a value ofTrue
for is_root
. You can use this to filter for root runs.
List runs without errors
List runs by run ID
Ignores Other ArgumentsIf you provide a list of run IDs in the way described above, it will ignore all other filtering arguments like
project_name
, run_type
, etc. and directly return the runs matching the given IDs.Use filter query language
For more complex queries, you can use the query language described in the filter query language reference.List all root runs in a conversational thread
This is the way to fetch runs in a conversational thread. For more information on setting up threads, refer to our how-to guide on setting up threads. Threads are grouped by setting a shared thread ID. The LangSmith UI lets you use any one of the following three metadata keys:session_id
, conversation_id
, or thread_id
. The session ID is also known as the tracing project ID. The following query matches on any of them.
List all runs called “extractor” whose root of the trace was assigned feedback “user_score” score of 1
List runs with “star_rating” key whose score is greater than 4
List runs that took longer than 5 seconds to complete
List all runs that have “error” not equal to null
List all runs where start_time is greater than a specific timestamp
List all runs that contain the string “substring”
List all runs that are tagged with the git hash “2aa1cf4”
List all runs that started after a specific timestamp and either have “error” not equal to null or a “Correctness” feedback score equal to 0
Complex query: List all runs where tags include “experimental” or “beta” and latency is greater than 2 seconds
Search trace trees by full text
You can use thesearch()
function without any specific field to do a full text search across all string fields in a run. This allows you to quickly find traces that match a search term.
Check for presence of metadata
If you want to check for the presence of metadata, you can use theeq
operator, optionally with an and
statement to match by value. This is useful if you want to log more structured information about your runs.
Check for environment details in metadata
A common pattern is to add environment information to your traces via metadata. If you want to filter for runs containing environment metadata, you can use the same pattern as above:Check for conversation ID in metadata
Another common way to associate traces in the same conversation is by using a shared conversation ID. If you want to filter runs based on a conversation ID in this way, you can search for that ID in the metadata.Negative filtering on key-value pairs
You can use negative filtering on metadata, input, and output key-value pairs to exclude specific runs from your results. Here are some examples for metadata key-value pairs but the same logic applies to input and output key-value pairs.Combine multiple filters
If you want to combine multiple conditions to refine your search, you can use theand
operator along with other filtering functions. Here’s how you can search for runs named “ChatOpenAI” that also have a specific conversation_id
in their metadata:
Tree Filter
List all runs named “RetrieveDocs” whose root run has a “user_score” feedback of 1 and any run in the full trace is named “ExpandQuery”. This type of query is useful if you want to extract a specific run conditional on various states or steps being reached within the trace.Advanced: export flattened trace view with child tool usage
The following Python example demonstrates how to export a flattened view of traces, including information on the tools (from nested runs) used by the agent within each trace. This can be used to analyze the behavior of your agents across multiple traces. This example queries all tool runs within a specified number of days and groups them by their parent (root) run ID. It then fetches the relevant information for each root run, such as the run name, inputs, outputs, and combines that information with the child run information. To optimize the query, the example:- Selects only the necessary fields when querying tool runs to reduce query time.
- Fetches root runs in batches while processing tool runs concurrently.