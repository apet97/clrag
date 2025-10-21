---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-data-export",
  "h1": "langsmith-data-export",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.449077",
  "sha256_raw": "ddd22f12a86f451320ec0c090a6b1ac991323814009ad5f87a3b6df8cc20a38a"
}
---

# langsmith-data-export

> Source: https://docs.langchain.com/langsmith/data-export

LangSmith’s bulk data export functionality allows you to export your traces into an external destination. This can be useful if you want to analyze the
data offline in a tool such as BigQuery, Snowflake, RedShift, Jupyter Notebooks, etc.
An export can be launched to target a specific LangSmith project and date range. Once a batch export is launched, our system will handle the orchestration and resilience of the export process.
Please note that exporting your data may take some time depending on the size of your data. We also have a limit on how many of your exports can run at the same time.
Bulk exports also have a runtime timeout of 24 hours.
Destinations
Currently we support exporting to an S3 bucket or S3 API compatible bucket that you provide. The data will be exported in Parquet columnar format. This format will allow you to easily import the data into other systems. The data export will contain equivalent data fields as the Run data format.Exporting Data
Destinations - Providing a S3 bucket
To export LangSmith data, you will need to provide an S3 bucket where the data will be exported to. The following information is needed for the export:- Bucket Name: The name of the S3 bucket where the data will be exported to.
- Prefix: The root prefix within the bucket where the data will be exported to.
- S3 Region: The region of the bucket - this is needed for AWS S3 buckets.
- Endpoint URL: The endpoint URL for the S3 bucket - this is needed for S3 API compatible buckets.
- Access Key: The access key for the S3 bucket.
- Secret Key: The secret key for the S3 bucket.
Preparing the Destination
For self-hosted and EU region deploymentsUpdate the LangSmith URL appropriately for self-hosted installations or organizations in the EU region in the requests below.
For the EU region, use
eu.api.smith.langchain.com
.Permissions requiredBoth the
backend
and queue
services require write access to the destination bucket:- The
backend
service attempts to write a test file to the destination bucket when the export destination is created. It will delete the test file if it has permission to do so (delete access is optional). - The
queue
service is responsible for bulk export execution and uploading the files to the bucket.
id
to reference this destination in subsequent bulk export operations.
If you receive an error while creating a destination, see debug destination errors for details on how to debug this.
Credentials configuration
Requires LangSmith Helm version >=
0.10.34
(application version >= 0.10.91
)access_key_id
and secret_access_key
:
- To use temporary credentials that include an AWS session token,
additionally provide the
credentials.session_token
key when creating the bulk export destination. - (Self-hosted only): To use environment-based credentials such as with AWS IAM Roles for Service Accounts (IRSA),
omit the
credentials
key from the request when creating the bulk export destination. In this case, the standard Boto3 credentials locations will be checked in the order defined by the library.
AWS S3 bucket
For AWS S3, you can leave off theendpoint_url
and supply the region that matches the region of your bucket.
Google GCS XML S3 compatible bucket
When using Google’s GCS bucket, you need to use the XML S3 compatible API, and supply theendpoint_url
which is typically https://storage.googleapis.com
.
Here is an example of the API request when using the GCS XML API which is compatible with S3:
Create an export job
To export data, you will need to create an export job. This job will specify the destination, the project, the date range, and filter expression of the data to export. The filter expression is used to narrow down the set of runs exported and is optional. Not setting the filter field will export all runs. Refer to our filter query language and examples to determine the correct filter expression for your export. You can use the following cURL command to create the job:The
session_id
is also known as the Tracing Project ID, which can be copied from the individual project view by clicking into the project in the Tracing Projects list.id
to reference this export in subsequent bulk export operations.
Scheduled exports
Requires LangSmith Helm version >=
0.10.42
(application version >= 0.10.109
)interval_hours
and remove end_time
:
interval_hours
must be between 1 hour and 168 hours (1 week) inclusive.- For spawned exports, the first time range exported is
start_time=(scheduled_export_start_time), end_time=(start_time + interval_hours)
. Thenstart_time=(previous_export_end_time), end_time=(this_export_start_time + interval_hours)
, and so on. end_time
must be omitted for scheduled exports.end_time
is still required for non-scheduled exports.- Scheduled exports can be stopped by cancelling the export.
- Exports that have been spawned by a scheduled export have the
source_bulk_export_id
attribute filled. - If desired, these spawned bulk exports must be canceled separately from the source scheduled bulk export - canceling the source bulk export does not cancel the spawned bulk exports.
- Exports that have been spawned by a scheduled export have the
- Spawned exports run at
end_time + 10 minutes
to account for any runs that are submitted withend_time
in the recent past.
start_time=2025-07-16T00:00:00Z
and interval_hours=6
:
| Export | Start Time | End Time | Runs At |
|---|---|---|---|
| 1 | 2025-07-16T00:00:00Z | 2025-07-16T06:00:00Z | 2025-07-16T06:10:00Z |
| 2 | 2025-07-16T06:00:00Z | 2025-07-16T12:00:00Z | 2025-07-16T12:10:00Z |
| 3 | 2025-07-16T12:00:00Z | 2025-07-16T18:00:00Z | 2025-07-16T18:10:00Z |
Monitoring the Export Job
Monitor Export Status
To monitor the status of an export job, use the following cURL command:{export_id}
with the ID of the export you want to monitor. This command retrieves the current status of the specified export job.
List Runs for an Export
An export is typically broken up into multiple runs which correspond to a specific date partition to export. To list all runs associated with a specific export, use the following cURL command:List All Exports
To retrieve a list of all export jobs, use the following cURL command:Stop an Export
To stop an existing export, use the following cURL command:{export_id}
with the ID of the export you wish to cancel. Note that a job cannot be restarted once it has been cancelled,
you will need to create a new export job instead.
Partitioning Scheme
Data will be exported into your bucket into the follow Hive partitioned format:Importing Data into other systems
Importing data from S3 and Parquet format is commonly supported by the majority of analytical systems. See below for documentation links:BigQuery
To import your data into BigQuery, see Loading Data from Parquet and also Hive Partitioned loads.Snowflake
You can load data into Snowflake from S3 by following the Load from Cloud Document.RedShift
You can COPY data from S3 / Parquet into RedShift by following the AWS COPY Instructions.Clickhouse
You can directly query data in S3 / Parquet format in Clickhouse. As an example, if using GCS, you can query the data as follows:DuckDB
You can query the data from S3 in-memory with SQL using DuckDB. See S3 import Documentation.Error Handling
Debugging Destination Errors
The destinations API endpoint will validate that the destination and credentials are valid and that write access is is present for the bucket. If you receive an error, and would like to debug this error, you can use the AWS CLI to test the connectivity to the bucket. You should be able to write a file with the CLI using the same data that you supplied to the destinations API above. AWS S3:--endpoint-url
option.
For GCS, the endpoint_url
is typically https://storage.googleapis.com
:
Monitoring Runs
You can monitor your runs using the List Runs API. If this is a known error, this will be added to theerrors
field of the run.
Common Errors
Here are some common errors:| Error | Description |
|---|---|
| Access denied | The blob store credentials or bucket are not valid. This error occurs when the provided access key and secret key combination doesn’t have the necessary permissions to access the specified bucket or perform the required operations. |
| Bucket is not valid | The specified blob store bucket is not valid. This error is thrown when the bucket doesn’t exist or there is not enough access to perform writes on the bucket. |
| Key ID you provided does not exist | The blob store credentials provided are not valid. This error occurs when the access key ID used for authentication is not a valid key. |
| Invalid endpoint | The endpoint_url provided is invalid. This error is raised when the specified endpoint is an invalid endpoint. Only S3 compatible endpoints are supported, for example https://storage.googleapis.com for GCS, https://play.min.io for minio, etc. If using AWS, you should omit the endpoint_url. |