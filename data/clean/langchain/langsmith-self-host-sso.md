---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-self-host-sso",
  "h1": "langsmith-self-host-sso",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.480174",
  "sha256_raw": "0984fe5f5cd06fa93a17eccf31e84128d12d79eeb515a8167a6119a3f737d1e6"
}
---

# langsmith-self-host-sso

> Source: https://docs.langchain.com/langsmith/self-host-sso

Overview
You may upgrade a basic auth installation to this mode, but not a none auth installation. In order to upgrade, simply remove the basic auth configuration and add the required configuration parameters as shown below. Users may then login via OAuth only. In order to maintain access post-upgrade, you must have access to login via OAuth using an email address that previously logged in via basic auth.
LangSmith does not support moving from SSO to basic auth mode in self-hosted at the moment. We also do not support moving from OAuth Mode with client secret to OAuth mode without a client secret and vice versa. Finally, we do not support having both basic auth and OAuth at the same time. Ensure you disable the basic auth configuration when enabling OAuth.
With Client Secret (Recommended)
By default, LangSmith Self-Hosted supports theAuthorization Code
flow with Client Secret
. In this version of the flow, your client secret is stored security in LangSmith (not on the frontend) and used for authentication and establishing auth sessions.
Prerequisites
- You must be self-hosted and on an Enterprise plan.
- Your IdP must support the
Authorization Code
flow withClient Secret
. - Your IdP must support using an external discovery/issuer URL. We will use this to fetch the necessary routes and keys for your IdP.
- You must provide the
OIDC
,email
, andprofile
scopes to LangSmith. We use these to fetch the necessary user information and email for your users.
LangSmith SSO is only supported over
https
.Configuration
- You will need to set the callback URL in your IdP to
https://<host>/api/v1/oauth/custom-oidc/callback
, wherehost
is the domain or IP you have provisioned for your LangSmith instance. This is where your IdP will redirect the user after they have authenticated. - You will need to provide the
oauthClientId
,oauthClientSecret
,hostname
, andoauthIssuerUrl
in yourvalues.yaml
file. This is where you will configure your LangSmith instance. - If you have not already configured Oauth with client secret or if you only have personal orgs, you must provide an email address to assign as the initial org admin for the newly provisioned SSO org. If you are upgrading from basic auth, your existing org will be reused instead.
Session length controls
All of the environment variables in this section are for the
platform-backend
service and can be added using platformBackend.deployment.extraEnv
in Helm.- By default, session length is controlled by the expiration of the identity token returned by the identity provider
- Most setups should use refresh tokens to enable session length extension beyond the identity token expiration up to
OAUTH_SESSION_MAX_SEC
, which may require including theoffline_access
scope by adding tooauthScopes
(Helm) orOAUTH_SCOPES
(Docker) OAUTH_SESSION_MAX_SEC
(default 1 day) can be overridden to a maximum of one week (604800
)- For identity provider setups that don’t support refresh tokens, setting
OAUTH_OVERRIDE_TOKEN_EXPIRY="true"
will takeOAUTH_SESSION_MAX_SEC
as the session length, ignoring the identity token expiration
Override Sub Claim
In some scenarios, it may be necessary to override which claim is used as thesub
claim from your identity provider.
For example, in SCIM, the resolved sub
claim and SCIM externalId
must match in order for login to succeed.
If there are restrictions on the source attribute of the sub
claim and/or the SCIM externalId
, set the ISSUER_SUB_CLAIM_OVERRIDES
environment variable to select which OIDC JWT claim is used as the sub
.
If an issuer URL starts with one of the URLs in this configuration, the sub
claim is taken from the field name specified.
For example, with the following configuration, a token with the issuer https://idp.yourdomain.com/application/uuid
would use the customClaim
value as the sub
:
oid
claim when Azure Entra ID is used as the identity provider:
Google Workspace IdP setup
You can use Google Workspace as a single sign-on (SSO) provider using OAuth2.0 and OIDC without PKCE.You must have administrator-level access to your organization’s Google Cloud Platform (GCP) account to create a new project, or permissions to create and configure OAuth 2.0 credentials for an existing project. We recommend that you create a new project for managing access, since each GCP project has a single OAuth consent screen.
- Create a new GCP project, see the Google documentation topic creating and managing projects
- After you have created the project, open the Credentials page in the Google API Console (making sure the project in the top left corner is correct)
-
Create new credentials:
Create Credentials → OAuth client ID
-
Choose
Web application
as theApplication type
and enter a name for the application e.g.LangSmith
-
In
Authorized Javascript origins
put the domain of your LangSmith instance e.g.https://langsmith.yourdomain.com
-
In
Authorized redirect URIs
put the domain of your LangSmith instance followed by/api/v1/oauth/custom-oidc/callback
e.g.https://langsmith.yourdomain.com/api/v1/oauth/custom-oidc/callback
-
Click
Create
, then download the JSON or copy and save theClient ID
(ends with.apps.googleusercontent.com
) andClient secret
somewhere secure. You will be able to access these later if needed. -
Select
OAuth consent screen
from the navigation menu on the left- Choose the Application type as
Internal
. If you selectPublic
, anyone with a Google account can sign in. - Enter a descriptive
Application name
. This name is shown to users on the consent screen when they sign in. For example, useLangSmith
or<organization_name> SSO for LangSmith
. - Verify that the Scopes for Google APIs only lists email, profile, and openid scopes. Only these scopes are required for single sign-on. If you grant additional scopes it increases the risk of exposing sensitive data.
- Choose the Application type as
- (Optional) control who within your organization has access to LangSmith: https://admin.google.com/ac/owl/list?tab=configuredApps. See Google’s documentation for additional details.
-
Configure LangSmith to use this OAuth application. For examples, here are the
config
values that would be used for Kubernetes configuration:oauthClientId
:Client ID
(ends with.apps.googleusercontent.com
)oauthClientSecret
:Client secret
hostname
: the domain of your LangSmith instance e.g.https://langsmith.yourdomain.com
(no trailing slash)oauthIssuerUrl
:https://accounts.google.com
oauth.enabled
:true
authType
:mixed
Okta IdP setup
Supported features
- IdP-initiated SSO
- SP-initiated SSO
Configuration steps
For additional information, see Okta’s documentation. If you have any questions or issues, please reach out to support@langchain.dev.Via Okta Integration Network (recommended)
This method of configuration is required in order to use SCIM with Okta.
- Sign in to Okta.
- In the upper-right corner, select Admin. The button is not visible from the Admin area.
- Select
Browse App Integration Catalog
. - Find and select the LangSmith application.
- On the application overview page, select Add Integration.
- Fill in
ApiUrlBase
:- Your LangSmith API URL without the protocol (
https://
) formatted as<langsmith_domain>/api/v1
, e.g.,langsmith.yourdomain.com/api/v1
. - If your installation is configured with a subdomain / path prefix, include that in the URL, e.g.,
langsmith.yourdomain.com/prefix/api/v1
.
- Your LangSmith API URL without the protocol (
- Leave
AuthHost
empty. - (Optional, if planning to use SCIM as well) Fill in
LangSmithUrl
: The<langsmith_url>
portion from above, e.g.,langsmith.yourdomain.com
. - Under Application Visibility, keep the box unchecked.
- Select Next.
- Select
OpenID Connect
. - Fill in
Sign-On Options
:Application username format
:Email
.Update application username on
:Create and update
.Allow users to securely see their password
: leave unchecked.
- Click Save.
- Configure LangSmith to use this OAuth application (see general configuration section for details about
initialOrgAdminEmail
):
Via Custom App Integration
- Log in to Okta as an administrator, and go to the Okta Admin console.
- Under Applications > Applications click Create App Integration.
- Select OIDC - OpenID Connect as the Sign-in method and Web Application as the Application type, then click Next.
- Enter an
App integration name
(e.g.,LangSmith
). - Recommended: Check Core grants > Refresh Token (see session length controls).
- In Sign-in redirect URIs put the domain of your LangSmith instance followed by
/api/v1/oauth/custom-oidc/callback
, e.g.,https://langsmith.yourdomain.com/api/v1/oauth/custom-oidc/callback
. If your installation is configured with a subdomain / path prefix, include that in the URL, e.g.,https://langsmith.yourdomain.com/prefix/api/v1/oauth/custom-oidc/callback
. - Remove the default URI under Sign-out redirect URIs.
- Under Trusted Origins > Base URIs add your langsmith URL with the protocol, e.g.,
https://langsmith.yourdomain.com
. - Select your desired option under Assignments > Controlled access:
- Allow everyone in your organization to access.
- Limit access to selected groups.
- Skip group assignment for now.
- Click Save.
- Under Sign On > OpenID Connect ID Token set Issuer to Okta URL.
- (Optional) Under General > Login set Login initiated by to
Either Okta or App
to enable IdP-initiated login. - (Recommended) Under General > Login > Email verification experience fill in the Callback URI with the LangSmith URL, e.g.,
https://langsmith.yourdomain.com
. - Configure LangSmith to use this OAuth application (see general configuration section for details about
initialOrgAdminEmail
):
SP-initiated SSO
Users can sign in using the Login via SSO button on the LangSmith homepage.Without Client Secret (PKCE) (Deprecated)
We recommend running with aClient Secret
if possible (previously we didn’t support this). However, if your IdP does not support this, you can use the Authorization Code with PKCE
flow.
This flow does not require a Client Secret
. For the alternative workflow, refer to With client secret.
Requirements
There are a couple of requirements for using OAuth SSO with LangSmith:- Your IdP must support the
Authorization Code with PKCE
flow (Google does not support this flow for example, but see above for an alternative configuration that Google supports). This is often displayed in your OAuth Provider as configuring a “Single Page Application (SPA)” - Your IdP must support using an external discovery/issuer URL. We will use this to fetch the necessary routes and keys for your IdP.
- You must provide the
OIDC
,email
, andprofile
scopes to LangSmith. We use these to fetch the necessary user information and email for your users. - You will need to set the callback URL in your IdP to
http://<host>/oauth-callback
, where host is the domain or IP you have provisioned for your LangSmith instance. This is where your IdP will redirect the user after they have authenticated. - You will need to provide the
oauthClientId
andoauthIssuerUrl
in yourvalues.yaml
file. This is where you will configure your LangSmith instance.