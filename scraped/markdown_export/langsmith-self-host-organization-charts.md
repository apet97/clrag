# langsmith-self-host-organization-charts

> Source: https://docs.langchain.com/langsmith/self-host-organization-charts

This feature is available on Helm chart versions 0.9.5 and later.
LangSmith automatically generates and syncs organization usage charts for self-hosted installations.
These charts are available under Settings > Usage and billing > Usage graph
:
- Usage by Workspace: this counts traces (root runs) by workspace
- Organization Usage: this counts all traces (root runs) for the organization
The charts are refreshed to include any new workspaces every 5 minutes. Note that the charts are not editable.
Programmatically fetch trace counts
You can retrieve trace counts programmatically using two different methods:
Method 1: Use the LangSmith REST API
If your self-hosted installation uses an online key, you can use the LangSmith REST API to fetch organization usage data.
Method 2: Use PostgreSQL support queries
For installations using offline keys or when you need more detailed export capabilities, you can run support queries directly against the PostgreSQL database. All available scripts are in the support queries repository.
For more detailed information about running support queries, see the Run support queries against PostgreSQL guide.