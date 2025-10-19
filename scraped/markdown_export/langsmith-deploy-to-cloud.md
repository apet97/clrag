# langsmith-deploy-to-cloud

> Source: https://docs.langchain.com/langsmith/deploy-to-cloud

Prerequisites
- LangSmith applications are deployed from GitHub repositories. Configure and upload a LangSmith application to a GitHub repository in order to deploy it to LangSmith.
- Verify that the LangGraph API runs locally. If the API does not run successfully (i.e.
langgraph dev
), deploying to LangSmith will fail as well.
Create New Deployment
Starting from the LangSmith UI:- In the left-hand navigation panel, select Deployments, which contains a list of existing deployments.
- In the top-right corner, select + New Deployment to create a new deployment.
- In the
Create New Deployment
panel, fill out the required fields. Deployment details
- Select
Import from GitHub
and follow the GitHub OAuth workflow to install and authorize LangChain’shosted-langserve
GitHub app to access the selected repositories. After installation is complete, return to theCreate New Deployment
panel and select the GitHub repository to deploy from the dropdown menu. Note: The GitHub user installing LangChain’shosted-langserve
GitHub app must be an owner of the organization or account. - Specify a name for the deployment.
- Specify the desired
Git Branch
. A deployment is linked to a branch. When a new revision is created, code for the linked branch will be deployed. The branch can be updated later in the Deployment Settings. - Specify the full path to the LangGraph API config file including the file name. For example, if the file
langgraph.json
is in the root of the repository, simply specifylanggraph.json
. - Check/uncheck checkbox to
Automatically update deployment on push to branch
. If checked, the deployment will automatically be updated when changes are pushed to the specifiedGit Branch
. This setting can be enabled/disabled later in the Deployment Settings. - Select the desired
Deployment Type
. Development
deployments are meant for non-production use cases and are provisioned with minimal resources.Production
deployments can serve up to 500 requests/second and are provisioned with highly available storage with automatic backups.- Determine if the deployment should be
Shareable through Studio
. - If unchecked, the deployment will only be accessible with a valid LangSmith API key for the workspace.
- If checked, the deployment will be accessible through Studio to any LangSmith user. A direct URL to Studio for the deployment will be provided to share with other LangSmith users.
- Specify
Environment Variables
and secrets. See the Environment Variables reference to configure additional variables for the deployment. - Sensitive values such as API keys (e.g.
OPENAI_API_KEY
) should be specified as secrets. - Additional non-secret environment variables can be specified as well.
- A new LangSmith
Tracing Project
is automatically created with the same name as the deployment. - In the top-right corner, select
Submit
. After a few seconds, theDeployment
view appears and the new deployment will be queued for provisioning.
Create New Revision
When creating a new deployment, a new revision is created by default. Subsequent revisions can be created to deploy new code changes. Starting from the LangSmith UI…- In the left-hand navigation panel, select Deployments, which contains a list of existing deployments.
- Select an existing deployment to create a new revision for.
- In the
Deployment
view, in the top-right corner, select+ New Revision
. - In the
New Revision
modal, fill out the required fields. - Specify the full path to the LangGraph API config file including the file name. For example, if the file
langgraph.json
is in the root of the repository, simply specifylanggraph.json
. - Determine if the deployment should be
Shareable through Studio
. - If unchecked, the deployment will only be accessible with a valid LangSmith API key for the workspace.
- If checked, the deployment will be accessible through Studio to any LangSmith user. A direct URL to Studio for the deployment will be provided to share with other LangSmith users.
- Specify
Environment Variables
and secrets. Existing secrets and environment variables are prepopulated. See the Environment Variables reference to configure additional variables for the revision. - Add new secrets or environment variables.
- Remove existing secrets or environment variables.
- Update the value of existing secrets or environment variables.
- Select
Submit
. After a few seconds, theNew Revision
modal will close and the new revision will be queued for deployment.
View Build and Server Logs
Build and server logs are available for each revision. Starting from the Deployments view:- Select the desired revision from the
Revisions
table. A panel slides open from the right-hand side and theBuild
tab is selected by default, which displays build logs for the revision. - In the panel, select the
Server
tab to view server logs for the revision. Server logs are only available after a revision has been deployed. - Within the
Server
tab, adjust the date/time range picker as needed. By default, the date/time range picker is set to theLast 7 days
.
View Deployment Metrics
Starting from the LangSmith UI…- In the left-hand navigation panel, select Deployments, which contains a list of existing deployments.
- Select an existing deployment to monitor.
- Select the
Monitoring
tab to view the deployment metrics. See a list of all available metrics. - Within the
Monitoring
tab, use the date/time range picker as needed. By default, the date/time range picker is set to theLast 15 minutes
.
Interrupt Revision
Interrupting a revision will stop deployment of the revision.Undefined Behavior
Interrupted revisions have undefined behavior. This is only useful if you need to deploy a new revision and you already have a revision “stuck” in progress. In the future, this feature may be removed.
- Select the menu icon (three dots) on the right-hand side of the row for the desired revision from the
Revisions
table. - Select
Interrupt
from the menu. - A modal will appear. Review the confirmation message. Select
Interrupt revision
.
Delete Deployment
Starting from the LangSmith UI…- In the left-hand navigation panel, select Deployments, which contains a list of existing deployments.
- Select the menu icon (three dots) on the right-hand side of the row for the desired deployment and select
Delete
. - A
Confirmation
modal will appear. SelectDelete
.
Deployment Settings
Starting from the Deployments view:- In the top-right corner, select the gear icon (
Deployment Settings
). - Update the
Git Branch
to the desired branch. - Check/uncheck checkbox to
Automatically update deployment on push to branch
. - Branch creation/deletion and tag creation/deletion events will not trigger an update. Only pushes to an existing branch will trigger an update.
- Pushes in quick succession to a branch will queue subsequent updates. Once a build completes, the most recent commit will begin building and the other queued builds will be skipped.
Add or Remove GitHub Repositories
After installing and authorizing LangChain’shosted-langserve
GitHub app, repository access for the app can be modified to add new repositories or remove existing repositories. If a new repository is created, it may need to be added explicitly.
- From the GitHub profile, navigate to
Settings
>Applications
>hosted-langserve
> clickConfigure
. - Under
Repository access
, selectAll repositories
orOnly select repositories
. IfOnly select repositories
is selected, new repositories must be explicitly added. - Click
Save
. - When creating a new deployment, the list of GitHub repositories in the dropdown menu will be updated to reflect the repository access changes.
Allowlisting IP Addresses
All traffic from LangSmith deployments created after January 6th 2025 will come through a NAT gateway. This NAT gateway will have several static ip addresses depending on the region you are deploying in. Refer to the table below for the list of IP addresses to allowlist:| US | EU |
|---|---|
| 35.197.29.146 | 34.90.213.236 |
| 34.145.102.123 | 34.13.244.114 |
| 34.169.45.153 | 34.32.180.189 |
| 34.82.222.17 | 34.34.69.108 |
| 35.227.171.135 | 34.32.145.240 |
| 34.169.88.30 | 34.90.157.44 |
| 34.19.93.202 | 34.141.242.180 |
| 34.19.34.50 | 34.32.141.108 |
| 34.59.244.194 | |
| 34.9.99.224 | |
| 34.68.27.146 | |
| 34.41.178.137 | |
| 34.123.151.210 | |
| 34.135.61.140 | |
| 34.121.166.52 | |
| 34.31.121.70 |