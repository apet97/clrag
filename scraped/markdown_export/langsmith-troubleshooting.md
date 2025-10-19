# langsmith-troubleshooting

> Source: https://docs.langchain.com/langsmith/troubleshooting

This guide will walk you through common issues you may encounter when running a self-hosted instance of LangSmith.While running LangSmith, you may encounter unexpected 500 errors, slow performance, or other issues. This guide will help you diagnose and resolve these issues.
To diagnose and resolve an issue, you will first need to retrieve some relevant information. Below, we explain how to do this for a kubernetes setup, a docker setup, as well as how to pull helpful browser info.Generally, the main services you will want to analyze are:
langsmith-backend: The main backend service.
langsmith-platform-backend: Another important backend service.
The first step in troubleshooting is to gather important debugging information about your LangSmith deployment. Service logs, kubernetes events, and resource utilization of containers can help identify the root cause of an issue.You can run our k8s troubleshooting script which will pull all of the relevant kubernetes information and output it to a folder for investigation. The script also compresses this folder into a zip file for sharing. Here is an example of how to run this script, assuming your langsmith deployment was brought up in a langsmith namespace:
You can then inspect the contents of the produced folder for any relevant errors or information. If you would like the LangSmith team to assist in debugging, please share this zip file with the team.
If you are experiencing an issue that surfaces as a browser error, it may also be helpful to inspect a HAR file which may include key information. To get the HAR file, you can follow this guide which explains the short process for various browsers.You can then use Google’s HAR analyzer to investigate. You can also send your HAR file to the LangSmith team to help with debugging.
In Kubernetes, you will need to increase the size of the ClickHouse PVC. To achieve this, you can perform the following steps:
Get the storage class of the PVC: kubectl get pvc data-langsmith-clickhouse-0 -n <namespace> -o jsonpath='{.spec.storageClassName}'
Ensure the storage class has AllowVolumeExpansion: true: kubectl get sc <storage-class-name> -o jsonpath='{.allowVolumeExpansion}'
If it is false, some storage classes can be updated to allow volume expansion.
To update the storage class, you can run kubectl patch sc <storage-class-name> -p '{"allowVolumeExpansion": true}'
If this fails, you may need to create a new storage class with the correct settings.
Edit your pvc to have the new size: kubectl edit pvc data-langsmith-clickhouse-0 -n <namespace> or kubectl patch pvc data-langsmith-clickhouse-0 '{"spec":{"resources":{"requests":{"storage":"100Gi"}}}}' -n <namespace>
Update your helm chart langsmith_config.yaml to new size(e.g 100 Gi)
error: Dirty database version ‘version’. Fix and force version
This error occurs when the ClickHouse database is in an inconsistent state with our migrations. You will need to reset to an earlier database version and then rerun your upgrade/migrations.
This error occurs when the request size exceeds the maximum allowed size. You will need to increase the maximum request size in your Nginx configuration.
Details: code: 497, message: default: Not enough privileges. To execute this query, it’s necessary to have the grant CREATE ROW POLICY ON default.feedbacks_rmt
This error occurs when your user does not have the necessary permissions to create row policies in Clickhouse. When deploying the Docker deployment, you need to copy the users.xml file from the github repo as well. This adds the <access_management> tag to the users.xml file, which allows the user to create row policies. Below is the default users.xml file that we expect to be used.
In some environments, your mount point may not be writable by the container. In these cases we suggest building a custom image with the users.xml file included.Example Dockerfile:
Copy
FROM clickhouse/clickhouse-server:24.8COPY ./users.xml /etc/clickhouse-server/users.d/users.xml
Then take the following steps:
Build your custom image.
Copy
docker build -t <image-name> .
Update your docker-compose.yaml to use the custom image. Make sure to remove the users.xml mount point.
ClickHouse fails to start up when running a cluster with AquaSec
In some environments, AquaSec may prevent ClickHouse from starting up correctly. This may manifest as the ClickHouse pod not emitting any logs and failing to get marked as ready.
Generally this is due to LD_PRELOAD being set by AquaSec, which interferes with ClickHouse. To resolve this, you can add the following environment variable to your ClickHouse deployment: