# langsmith-data-purging-compliance

> Source: https://docs.langchain.com/langsmith/data-purging-compliance

Data retention
LangSmith provides automatic data retention capabilities to help with compliance and storage management. Data retention policies can be configured at the organization and project levels. For detailed information about data retention configuration and management, please refer to the Data Retention concepts documentation.Trace deletes
You can use the API to complete trace deletes. The API supports two methods for deleting traces:- By trace IDs and session ID: Delete specific traces by providing a list of trace IDs and their corresponding session ID (up to 1000 traces per request)
- By metadata: Delete traces across a workspace that match any of the specified metadata key-value pairs
All trace deletions will delete related entities like feedbacks, aggregations, and stats across all data storages.
Deletion timeline
Trace deletions are processed during non-peak usage times and are not instant, usually within a few hours. There is no confirmation of deletion - you’ll need to query the data again to verify it has been removed.Delete specific traces
To delete specific traces by their trace IDs from a single session:Delete by metadata
When deleting by metadata:- Accepts a
metadata
object of key/value pairs. KV pair matching uses an or condition. A trace will match if it has any of the key-value pairs specified in metadata (not all) - You don’t need to specify a session id when deleting by metadata. Deletes will apply across the workspace.
user_id: "user123"
or environment: "staging"
in their metadata.
Remember that you can only schedule up to 1000 traces per session per request. For larger deletions, you’ll need to make multiple requests.
Example deletes
You can delete dataset examples self-serve via our API, which supports both soft and hard deletion methods depending on your data retention needs.Hard deletes will permanently remove inputs, outputs, and metadata from ALL versions of the specified examples across the entire dataset history.
Deleting examples is a two-step process
For bulk operations, example deletion follows a two-step process:1. Search for examples by metadata
Find all examples with matching metadata across all datasets in a workspace. GET /examplesas_of
must be explicitly specified as a timestamp. Only examples created before theas_of
date will be returned
user_id: "user123"
or environment: "staging"
in their metadata across all datasets in your workspace.
2. Hard delete examples
Once you have the example IDs, send a delete request. This will zero-out the inputs, outputs, and metadata from all versions of the dataset for that example. DELETE /examples- Specify example IDs and add
"hard_delete": true
to the query params of the request
Deletion types
Soft delete (default)
- Creates tombstoned entries with NULL inputs/outputs in the dataset
- Preserves historical data and maintains dataset versioning
- Only affects the current version of the dataset
Hard delete
- Permanently removes inputs, outputs, and metadata from ALL dataset versions
- Complete data removal when compliance requires zero-out across all versions
- Add
"hard_delete": true
to the query parameters