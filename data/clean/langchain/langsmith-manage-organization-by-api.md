---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-manage-organization-by-api",
  "h1": "langsmith-manage-organization-by-api",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.445924",
  "sha256_raw": "8831fd502ac339c62a5ec5514ca2513fa096a56596e0e35da6729675f82d3ccf"
}
---

# langsmith-manage-organization-by-api

> Source: https://docs.langchain.com/langsmith/manage-organization-by-api

There are a few limitations that will be lifted soon:
- The LangSmith SDKs do not support these organization management actions yet.
- Organization-scoped service keys with Organization Admin permission may be used for these actions.
Use the
X-Tenant-Id
header to specify which workspace to target. If the header is not present, operations will default to the workspace the API key was initially created in if it is not organization-scoped.If X-Tenant-Id
is not specified when accessing workspace-scoped resources with an organization-scoped API key, the request will fail with 403 Forbidden
.X-Organization-Id
header should be present on all requests, and X-Tenant-Id
header should be present on requests that are scoped to a particular workspace.
Workspaces
User management
RBAC
Membership management
List roles
under RBAC should be used for retrieving role IDs of these operations. List [organization|workspace] members
endpoints (below) response "id"
s should be used as identity_id
in these operations.
Organization level:
- List active organization members
- List pending organization members
- Invite a user to the organization and one or more workspaces. This should be used when the user is not already a member in the organization.
- Update a user’s organization role
- Remove someone from the organization
- List workspace members
- Add a member to a workspace that is already part of the organization
- Update a user’s workspace role
- Remove someone from a workspace
API keys
Security settings
Updating these settings affects all resources in the organization.
- Update organization sharing settings
- use
unshare_all
to unshare ALL shared resources in the organization - usedisable_public_sharing
to prevent future sharing of resources
- use
User-only endpoints
These endpoints are user-scoped and require a logged-in user’s JWT, so they should only be executed through the UI./api-key/current
endpoints: these are related a user’s PATs/sso/email-verification/send
(Cloud-only): this endpoint is related to SAML SSO
Sample code
The sample code below goes through a few common workflows related to organization management. Make sure to make necessary replacements wherever<replace_me>
is in the code.