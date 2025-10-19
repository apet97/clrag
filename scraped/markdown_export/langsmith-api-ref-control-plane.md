# langsmith-api-ref-control-plane

> Source: https://docs.langchain.com/langsmith/api-ref-control-plane

Host
The control plane hosts for Cloud data regions:| US | EU |
|---|---|
https://api.host.langchain.com | https://eu.api.host.langchain.com |
/api-host
. For example, http(s)://<host>/api-host/v2/deployments
. See here for more details.
Authentication
To authenticate with the control plane API, set theX-Api-Key
header to a valid LangSmith API key.
Example curl
command:
Versioning
Each endpoint path is prefixed with a version (e.g.v1
, v2
).
Quick Start
- Call
POST /v2/deployments
to create a new Deployment. The response body contains the Deployment ID (id
) and the ID of the latest (and first) revision (latest_revision_id
). - Call
GET /v2/deployments/{deployment_id}
to retrieve the Deployment. Setdeployment_id
in the URL to the value of Deployment ID (id
). - Poll for revision
status
untilstatus
isDEPLOYED
by callingGET /v2/deployments/{deployment_id}/revisions/{latest_revision_id}
. - Call
PATCH /v2/deployments/{deployment_id}
to update the deployment.