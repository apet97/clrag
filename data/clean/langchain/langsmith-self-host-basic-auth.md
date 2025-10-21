---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-self-host-basic-auth",
  "h1": "langsmith-self-host-basic-auth",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.461671",
  "sha256_raw": "725d608928353852ae9922831911bc564b3b20009e1edce5563c588790112528"
}
---

# langsmith-self-host-basic-auth

> Source: https://docs.langchain.com/langsmith/self-host-basic-auth

- You cannot change an existing installation from basic auth mode to OAuth with PKCE (deprecated) or vice versa - installations must be either one or the other. A basic auth installation requires a completely fresh installation including a separate PostgreSQL database/schema, unless migrating from an existing
None
type installation (see below). - Users must be given their initial auto-generated password once they are invited. This password may be changed later by any Organization Admin.
- You cannot use both basic auth and OAuth with client secret at the same time.
Requirements and features
- There is a single
Default
organization that is provisioned during initial installation, and creating additional organizations is not supported - Your initial password (configured below) must be least 12 characters long and have at least one lowercase, uppercase, and symbol
- There are no strict requirements for the secret used for signing JWTs, but we recommend securely generating a string of at least 32 characters. For example:
openssl rand -base64 32
Migrating from None auth
Only supported in versions 0.7 and above. Migrating an installation from None auth mode replaces the single “default” user with a user with the configured credentials and keeps all existing resources. The single pre-existing workspace ID post-migration remains00000000-0000-0000-0000-000000000000
, but everything else about the migrated installation is standard for a basic auth installation.
To migrate, simply update your configuration as shown below and run helm upgrade
(or docker-compose up
) as usual.
Configuration
Changing the JWT secret will log out your users
initialOrgAdminEmail
and initialOrgAdminPassword
values, and your user will be auto-provisioned with role Organization Admin
. See the admin guide for more details on organization roles.