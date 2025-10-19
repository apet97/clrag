# langsmith-self-host-blob-storage

> Source: https://docs.langchain.com/langsmith/self-host-blob-storage

- In high trace environments, inputs, outputs, errors, manifests, extras, and events may balloon the size of your databases.
- If using LangSmith Managed ClickHouse, you may want sensitive information in blob storage that resides in your environment. To alleviate this, LangSmith supports storing run inputs, outputs, errors, manifests, extras, events, and attachments in an external blob storage system.
Requirements
- Access to a valid blob storage service
-
A bucket/directory in your blob storage to store the data. We highly recommend creating a separate bucket/directory for LangSmith data.
- If you are using TTLs, you will need to set up a lifecycle policy to delete old data. You can find more information on configuring TTLs here. These policies should mirror the TTLs you have set in your LangSmith configuration, or you may experience data loss. See here on how to setup the lifecycle rules for TTLs for blob storage.
-
Credentials to permit LangSmith Services to access the bucket/directory
- You will need to provide your LangSmith instance with the necessary credentials to access the bucket/directory. Read the authentication section below for more information.
-
If using S3 or GCS, an API url for your blob storage service
- This will be the URL that LangSmith uses to access your blob storage system
- For Amazon S3, this will be the URL of the S3 endpoint. Something like:
https://s3.amazonaws.com
orhttps://s3.us-west-1.amazonaws.com
if using a regional endpoint. - For Google Cloud Storage, this will be the URL of the GCS endpoint. Something like:
https://storage.googleapis.com
Authentication
Amazon S3
To authenticate to Amazon S3, you will need to create an IAM policy granting the following permissions on your bucket.-
(Recommended) IAM Role for Service Account: You can create an IAM role for your LangSmith instance and attach the policy to that role. You can then provide the role to LangSmith. This is the recommended way to authenticate with Amazon S3 in production.
- You will need to create an IAM role with the policy attached.
- You will need to allow LangSmith service accounts to assume the role. The
langsmith-queue
,langsmith-backend
, andlangsmith-platform-backend
service accounts will need to be able to assume the role.The service account names will be different if you are using a custom release name. You can find the service account names by runningkubectl get serviceaccounts
in your cluster. - You will need to provide the role ARN to LangSmith. You can do this by adding the
eks.amazonaws.com/role-arn: "<role_arn>"
annotation to thequeue
,backend
, andplatform-backend
services in your Helm Chart installation.
-
Access Key and Secret Key: You can provide LangSmith with an access key and secret key. This is the simplest way to authenticate with Amazon S3. However, it is not recommended for production use as it is less secure.
- You will need to create a user with the policy attached. Then you can provision an access key and secret key for that user.
-
VPC Endpoint Access: You can enable access to your S3 bucket via a VPC endpoint, which allows traffic to flow securely from your VPC to your S3 bucket.
- You’ll need to provision a VPC endpoint and configure it to allow access to your S3 bucket.
- You can refer to our public Terraform modules for guidance and an example of configuring this.
KMS encryption header support for S3
Starting with LangSmith Helm chart version 0.11.24, you can pass a KMS encryption key header and enforce a specific KMS key for writes by providing its ARN. To enable this, set the following values in your Helm chart:Helm
Google Cloud Storage
To authenticate with Google Cloud Storage, you will need to create aservice account
with the necessary permissions to access your bucket.
Your service account will need the Storage Admin
role or a custom role with equivalent permissions. This can be scoped to the bucket that LangSmith will be using.
Once you have a provisioned service account, you will need to generate a HMAC key
for that service account. This key and secret will be used to authenticate with Google Cloud Storage.
Azure Blob Storage
To authenticate with Azure Blob Storage, you will need to use one of the following methods to grant LangSmith workloads permission to access your container (listed in order of precedence):- Storage account and access key
- Connection string
- Workload identity (recommended), managed identity, or environment variables supported by
DefaultAzureCredential
. This is the default authentication method when configuration for either option above is not present.- To use workload identity, add the label
azure.workload.identity/use: true
to thequeue
,backend
, andplatform-backend
deployments. Additionally, add theazure.workload.identity/client-id
annotation to the corresponding service accounts, which should be an existing Azure AD Application’s client ID or user-assigned managed identity’s client ID. See Azure’s documentation for additional details.
- To use workload identity, add the label
Some deployments may need further customization of the connection configuration using a Service URL Override instead of the default service URL (
https://<storage_account_name>.blob.core.windows.net/
). For example, this override is necessary in order to use a different blob storage domain (e.g. government or china).CH Search
By default, LangSmith will still store tokens for search in ClickHouse. If you are using LangSmith Managed Clickhouse, you may want to disable this feature to avoid sending potentially sensitive information to ClickHouse. You can do this in your blob storage configuration.Configuration
After creating your bucket and obtaining the necessary credentials, you can configure LangSmith to use your blob storage system.If using an access key and secret, you can also provide an existing Kubernetes secret that contains the authentication information. This is recommended over providing the access key and secret key directly in your config. See the generated secret template for the expected secret keys.
TTL Configuration
If using the TTL feature with LangSmith, you’ll also have to configure TTL rules for your blob storage. Trace information stored on blob storage is stored on a particular prefix path, which determines the TTL for the data. When a trace’s retention is extended, its corresponding blob storage path changes to ensure that it matches the new extended retention. The following TTL prefix are used:ttl_s/
: Short term TTL, configured for 14 days.ttl_l/
: Long term TTL, configured for 400 days.