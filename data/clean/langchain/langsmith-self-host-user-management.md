---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-self-host-user-management",
  "h1": "langsmith-self-host-user-management",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.483179",
  "sha256_raw": "b561221ec4a68cb361c69d6ac8a2d152b45611693dab30b955e513f6321f7de4"
}
---

# langsmith-self-host-user-management

> Source: https://docs.langchain.com/langsmith/self-host-user-management

Features
Workspace level invites to an organization
The default behavior in LangSmith requires a user to be an Organization Admin in order to invite new users to an organization. For self-hosted customers that would like to delegate this responsibility to workspace Admins, a feature flag may be set that enables workspace Admins to invite new users to the organization as well as their specific workspace at the workspace level. Once this feature is enabled via the configuration option below, workspace Admins may add new users in theWorkspace members
tab under Settings
> Workspaces
. Both of the following cases are supported when inviting at the workspace level, while the organization level invite functions the same as before.
- Invite users who are NOT already active in the organization: this will add the users as pending to the organization and specific workspace
- Invite users who ARE already active in the organization: adds the users directly to the workspace as an active member (no pending state).
Configuration
SSO New Member Login Flow
As of helm v0.11.10, self-hosted deployments using OAuth SSO will no longer need to manually add members in LangSmith settings for them to join. Deployments will have a default organization, to which new users will automatically be added upon their first login to LangSmith. For your default organization, you can set which workspace(s) and workspace role is assigned to new members. For non-default organizations, the invitation flow remains the same. Once a user joins an organization, any changes to their workspaces or roles beyond the default organization settings must be managed either through LangSmith settings (as before) or via SCIM.By default, all new users are added to the organization’s initially provisioned workspace (Workspace 1 by default) with the Workspace Editor role.
To change your default organization, use Set Default Organization in the organization selector dropdown. (Org Admin permissions required in both the source and target organization.)