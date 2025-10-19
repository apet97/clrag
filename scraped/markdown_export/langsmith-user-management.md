# langsmith-user-management

> Source: https://docs.langchain.com/langsmith/user-management

- Set up access control: Configure role-based access control (RBAC) to manage user permissions within workspaces, including creating custom roles and assigning them to users.
- SAML SSO (Enterprise plan): Set up Single Sign-On authentication for Enterprise customers using SAML 2.0, including configuration for popular identity providers.
- SCIM User Provisioning (Enterprise plan): Automate user provisioning and deprovisioning between your identity provider and LangSmith using SCIM.
Set up access control
RBAC (Role-Based Access Control) is a feature that is only available to Enterprise customers. If you are interested in this feature, contact our sales team. Other plans default to using the
Admin
role for all users.workspace:manage
permission can manage access control settings for a workspace.
Create a role
By default, LangSmith comes with a set of system roles:Admin
: has full access to all resources within the workspace.Viewer
: has read-only access to all resources within the workspace.Editor
: has full permissions except for workspace management (adding/removing users, changing roles, configuring service keys).
Organization Admins
can create custom roles to suit your needs.
To create a role, navigate to the Roles tab in the Members and roles section of the Organization settings page. Note that new roles that you create will be usable across all workspaces within your organization.
Click on the Create Role button to create a new role. A Create role form will open.
Assign permissions for the different LangSmith resources that you want to control access to.
Assign a role to a user
Once you have your roles set up, you can assign them to users. To assign a role to a user, navigate to theWorkspace members
tab in the Workspaces
section of the Organization settings page
Each user will have a Role dropdown that you can use to assign a role to them.
You can also invite new users with a given role.
Set up SAML SSO for your organization
Single Sign-On (SSO) functionality is available for Enterprise Cloud customers to access LangSmith through a single authentication source. This allows administrators to centrally manage team access and keeps information more secure. LangSmith’s SSO configuration is built using the SAML (Security Assertion Markup Language) 2.0 standard. SAML 2.0 enables connecting an Identity Provider (IdP) to your organization for an easier, more secure login experience. SSO services permit a user to use one set of credentials (for example, a name or email address and password) to access multiple applications. The service authenticates the end user only once for all the applications the user has been given rights to and eliminates further prompts when the user switches applications during the same session. The benefits of SSO include:- Streamlines user management across systems for organization owners.
- Enables organizations to enforce their own security policies (e.g., MFA).
- Removes the need for end users to remember and manage multiple passwords. Simplifies the end-user experience, by allowing sign in at one single access point across multiple applications.
Just-in-time (JIT) provisioning
User invites are not supported in organizations with SAML SSO enabled. Initial workspace membership and role is determined by JIT provisioning, and changes afterwards can be managed in the UI.
For additional flexibility in automated user management, LangSmith supports SCIM.
Login methods and access
Once you have completed your configuration of SAML SSO for your organization, users will be able to log in via SAML SSO in addition to other login methods, such as username/password or Google Authentication”:- When logged in via SAML SSO, users can only access the corresponding organization with SAML SSO configured.
- Users with SAML SSO as their only login method do not have personal organizations.
- When logged in via any other method, users can access the organization with SAML SSO configured along with any other organizations they are a part of.
Enforce SAML SSO only
To ensure users can only access the organization when logged in using SAML SSO and no other method, check the Login via SSO only checkbox and click Save. Once this happens, users accessing the organization that are logged-in via a non-SSO login method are required to log back in using SAML SSO. This setting can be switched back to allow all login methods by unselecting the checkbox and clicking Save.You must be logged in via SAML SSO in order to update this setting to
Only SAML SSO
. This is to ensure the SAML settings are valid and avoid locking users out of your organization.Prerequisites
- Your organization must be on an Enterprise plan.
- Your Identity Provider (IdP) must support the SAML 2.0 standard.
- Only
Organization Admins
can configure SAML SSO.
Initial configuration
-
In your IdP: Configure a SAML application with the following details, then copy the metadata URL or XML for step 3.
The following URLs are different for the US and EU regions. Ensure you select the correct link.
- Single sign-on URL (or ACS URL):
- Audience URI (or SP Entity ID):
- Name ID format: email address.
- Application username: email address.
- Required claims:
sub
andemail
.
-
In LangSmith: Go to Settings -> Members and roles -> SSO Configuration. Fill in the required information and submit to activate SSO login:
- Fill in either the
SAML metadata URL
orSAML metadata XML
. - Select the
Default workspace role
andDefault workspaces
. New users logging in via SSO will be added to the specified workspaces with the selected role.
- Fill in either the
Default workspace role
andDefault workspaces
are editable. The updated settings will apply to new users only, not existing users.- (Coming soon)
SAML metadata URL
andSAML metadata XML
are editable. This is usually only necessary when cryptographic keys are rotated/expired or the metadata URL has changed but the same IdP is still used.
Entra ID (Azure)
For additional information, see Microsoft’s documentation. Step 1: Create a new Entra ID application integration-
Log in to the Azure portal with a privileged role (e.g.,
Global Administrator
). On the left navigation pane, select theEntra ID
service. - Navigate to Enterprise Applications and then select All Applications.
- Click Create your own application.
-
In the Create your own application window:
- Enter a name for your application (e.g.,
LangSmith
). - Select *Integrate any other application you don’t find in the gallery (Non-gallery)**.
- Enter a name for your application (e.g.,
- Click Create.
- Open the enterprise application that you created.
- In the left-side navigation, select Manage > Single sign-on.
- On the Single sign-on page, click SAML.
-
Update the Basic SAML Configuration:
Identifier (Entity ID)
:Reply URL (Assertion Consumer Service URL)
:- Leave
Relay State
,Logout Url
, andSign on URL
empty. - Click Save.
-
Ensure required claims are present with Namespace:
http://schemas.xmlsoap.org/ws/2005/05/identity/claims
:sub
:user.objectid
.emailaddress
:user.userprincipalname
oruser.mail
(if using the latter, ensure all users have theEmail
field filled in underContact Information
).- (Optional) For SCIM, see the setup documentation for specific instructions about
Unique User Identifier (Name ID)
.
- On the SAML-based Sign-on page, under SAML Certificates, copy the App Federation Metadata URL.
Fill in required information
step, using the metadata URL from the previous step.
Step 4: Verify the SSO setup
-
Assign the application to users/groups in Entra ID:
- Select Manage > Users and groups.
- Click Add user/group.
-
In the Add Assignment window:
- Under Users, click None Selected.
- Search for the user you want to assign to the enterprise application, and then click Select.
- Verify that the user is selected, and click Assign.
- Have the user sign in via the unique login URL from the SSO Configuration page, or go to Manage > Single sign-on and select Test single sign-on with (application name).
- Make sure you’re signed into an administrator account with the appropriate permissions.
- In the Admin console, go to Menu -> Apps -> Web and mobile apps.
- Click Add App and then Add custom SAML app.
- Enter the app name and, optionally, upload an icon. Click Continue.
- On the Google Identity Provider details page, download the IDP metadata and save it for Step 2. Click Continue.
-
In the
Service Provider Details
window, enter:ACS URL
:Entity ID
:- Leave
Start URL
and theSigned response
box empty. - Set
Name ID
format toEMAIL
and leaveName ID
as the default (Basic Information > Primary email
). - Click
Continue
.
-
Use
Add mapping
to ensure required claims are present:Basic Information > Primary email
->email
Fill in required information
step, using the IDP metadata
from the previous step as the metadata XML.
Step 3: Turn on the SAML app in Google
-
Select the SAML app under
Menu -> Apps -> Web and mobile apps
-
Click
User access
. -
Turn on the service:
-
To turn the service on for everyone in your organization, click
On for everyone
, and then clickSave
. -
To turn the service on for an organizational unit:
- At the left, select the organizational unit then
On
. - If the Service status is set to
Inherited
and you want to keep the updated setting, even if the parent setting changes, clickOverride
. - If the Service status is set to
Overridden
, either clickInherit
to revert to the same setting as its parent, or clickSave
to keep the new setting, even if the parent setting changes.
- At the left, select the organizational unit then
- To turn on a service for a set of users across or within organizational units, select an access group. For details, go to Use groups to customize service access.
-
To turn the service on for everyone in your organization, click
- Ensure that the email addresses your users use to sign in to LangSmith match the email addresses they use to sign in to your Google domain.
Okta
Supported features
- IdP-initiated SSO (Single Sign-On)
- SP-initiated SSO
- Just-In-Time provisioning
- Enforce SSO only
Configuration steps
For additional information, see Okta’s documentation. Step 1: Create and configure the Okta SAML applicationVia Okta Integration Network (recommended)
- Sign in to Okta.
- In the upper-right corner, select Admin. The button is not visible from the Admin area.
- Select
Browse App Integration Catalog
. - Find and select the LangSmith application.
- On the application overview page, select Add Integration.
- Leave
ApiUrlBase
empty. - Fill in
AuthHost
:- US:
auth.langchain.com
- EU:
eu.auth.langchain.com
- US:
- (Optional, if planning to use SCIM as well) Fill in
LangSmithUrl
:- US:
api.smith.langchain.com
- EU:
eu.api.smith.langchain.com
- US:
- Under Application Visibility, keep the box unchecked.
- Select Next.
- Select
SAML 2.0
. - Fill in
Sign-On Options
:Application username format
:Email
Update application username on
:Create and update
Allow users to securely see their password
: leave unchecked.
- Copy the Metadata URL from the Sign On Options page to use in the next step.
- Log in to Okta as an administrator, and go to the Okta Admin console.
- Under Applications > Applications click Create App Integration.
- Select SAML 2.0.
-
Enter an
App name
(e.g.,LangSmith
) and optionally an App logo, then click Next. -
Enter the following information in the Configure SAML page:
Single sign-on URL
(ACS URL
). KeepUse this for Recipient URL and Destination URL
checked:Audience URI (SP Entity ID)
:Name ID format
: Persistent.Application username
:email
.- Leave the rest of the fields empty or set to their default.
- Click Next.
- Click Finish.
- Copy the Metadata URL from the Sign On page to use in the next step.
- Under Applications > Applications, select the SAML application created in Step 1.
- Under the Assignments tab, click Assign then either Assign to People or Assign to Groups.
- Make the desired selection(s), then Assign and Done.
SSO Configuration
page, or have a user select the application from their Okta dashboard.
SP-initiated SSO
Once service-provider–initiated SSO is configured, users can sign in using a unique login URL. You can find this in the LangSmith UI under Organization members and roles then SSO configuration.Set up SCIM for your organization
System for Cross-domain Identity Management (SCIM) is an open standard that allows for the automation of user provisioning. Using SCIM, you can automatically provision and de-provision users in your LangSmith organization and workspaces, keeping user access synchronized with your organization’s identity provider.SCIM is available for organizations on the Enterprise plan. Contact sales to learn more.SCIM is available on Helm chart versions 0.10.41 (application version 0.10.108) and later.SCIM support is API-only (see instructions below).
- Automated user management: Users are automatically added, updated, and removed from LangSmith based on their status in your IdP.
- Reduced administrative overhead: No need to manage user access manually across multiple systems.
- Improved security: Users who leave your organization are automatically deprovisioned from LangSmith.
- Consistent access control: User attributes and group memberships are synchronized between systems.
- Scaling team access control: Efficiently manage large teams with many workspaces and custom roles.
- Role assignment: Select specific Organization Roles and Workspace Roles for groups of users.
Requirements
Prerequisites
- Your organization must be on an Enterprise plan.
- Your Identity Provider (IdP) must support SCIM 2.0.
- Only Organization Admins can configure SCIM.
- For cloud customers: SAML SSO must be configurable for your organization.
- For self-hosted customers: OAuth with Client Secret authentication mode must be enabled.
- For self-hosted customers, network traffic must be allowed from the identity provider to LangSmith:
Role Precedence
When a user belongs to multiple groups for the same workspace, the following precedence applies:- Organization Admin groups take highest precedence. Users in these groups will be
Admin
in all workspaces. - Most recently created workspace-specific group takes precedence over other workspace groups.
When a group is deleted or a user is removed from a group, their access is updated according to their remaining group membership, following the precedence rules.SCIM group membership will override manually assigned roles or roles assigned via Just-in-time (JIT) provisioning. We recommend disabling JIT provisioning to avoid conflicts.
Email verification
In cloud only, creating a new user with SCIM triggers an email to the user. They must verify their email address by clicking the link in this email. The link expires in 24 hours, and can be resent if needed by removing and re-adding the user via SCIM.Attributes and Mapping
Group Naming Convention
Group membership maps to LangSmith workspace membership and workspace roles with a specific naming convention: Organization Admin Groups Format:<optional_prefix>Organization Admin
or <optional_prefix>Organization Admins
Examples:
LS:Organization Admins
Groups-Organization Admins
Organization Admin
<optional_prefix><org_role_name>:<workspace_name>:<workspace_role_name>
Examples:
LS:Organization User:Production:Annotators
Groups-Organization User:Engineering:Developers
Organization User:Marketing:Viewers
Mapping
While specific instructions depending on the identity provider may vary, these mappings show what is supported by the LangSmith SCIM integration:User Attributes
| LangSmith App Attribute | Identity Provider Attribute | Matching Precedence |
|---|---|---|
userName 1 | email address | |
active | !deactivated | |
emails[type eq "work"].value | email address2 | |
name.formatted | displayName OR givenName + familyName 3 | |
givenName | givenName | |
familyName | familyName | |
externalId | sub 4 | 1 |
userName
is not required by LangSmith- Email address is required
- Use the computed expression if your
displayName
does not match the format ofFirstname Lastname
- To avoid inconsistency, this should match the SAML
NameID
assertion for cloud customers, or thesub
OAuth2.0 claim for self-hosted.
Group Attributes
| LangSmith App Attribute | Identity Provider Attribute | Matching Precedence |
|---|---|---|
displayName | displayName 1 | 1 |
externalId | objectId | |
members | members |
- Groups must follow the naming convention described in the Group Naming Convention section.
If your company has a group naming policy, you should instead map from the
description
identity provider attribute and set the description based on the Group Naming Convention section.
Step 1 - Configure SAML SSO (Cloud only)
There are two scenarios for SAML SSO configuration:- If SAML SSO is already configured for your organization, you should skip the steps to initially add the application (Add application from Okta Integration Network or Create a new Entra ID application integration), as you already have an application configured and just need to enable provisioning.
- If you are configuring SAML SSO for the first time alongside SCIM, first follow the instructions to set up SAML SSO, then follow the instructions here to enable SCIM.
NameID Format
LangSmith uses the SAML NameID to identify users. The NameID is a required field in the SAML response and is case-insensitive. The NameID must:- Be unique to each user.
- Be a persistent value that never changes, such as a randomly generated unique user ID.
- Match exactly on each sign-in attempt. It should not rely on user input.
Persistent
, unless you are using a field, like email, that requires a different format.
Step 2 - Disable JIT provisioning
Before enabling SCIM, disable Just-in-time (JIT) provisioning to prevent conflicts between automatic and manual user provisioning.Disabling JIT for Cloud
Use thePATCH /orgs/current/info
endpoint:
Disabling JIT for Self-Hosted
As of LangSmith chart version 0.11.14, you can disable JIT provisioning for your self-hosted organization using SSO. To disable, set the following values:Step 3 - Generate SCIM bearer token
In self-hosted environments, the full URL below may look like
https://langsmith.yourdomain.com/api/v1/platform/orgs/current/scim/tokens
(without a subdomain, note the /api/v1
path prefix) or https://langsmith.yourdomain.com/subdomain/api/v1/platform/orgs/current/scim/tokens
(with a subdomain) - see the ingress docs for more details.GET /v1/platform/orgs/current/scim/tokens
GET /v1/platform/orgs/current/scim/tokens/{scim_token_id}
PATCH /v1/platform/orgs/current/scim/tokens/{scim_token_id}
(only thedescription
field is supported)DELETE /v1/platform/orgs/current/scim/tokens/{scim_token_id}
Step 4 - Configure your Identity Provider
If you use Azure Entra ID (formerly Azure AD) or Okta, there are specific instructions for identity provider setup (refer to Azure Entra ID, Okta). The requirements and steps above are applicable for all identity providers.
Azure Entra ID configuration steps
For additional information, see Microsoft’s documentation.
Step 1: Configure SCIM in your Enterprise Application
- Log in to the Azure portal with a privileged role (e.g.,
Global Administrator
). - Navigate to your existing LangSmith Enterprise Application.
- In the left-side navigation, select Manage > Provisioning.
- Click Get started.
-
Under Admin Credentials:
-
Tenant URL:
- US:
https://api.smith.langchain.com/scim/v2
- EU:
https://eu.api.smith.langchain.com/scim/v2
- Self-hosted:
<langsmith_url>/scim/v2
- US:
- Secret Token: Enter the SCIM Bearer Token generated in Step 3.
-
Tenant URL:
- Click Test Connection to verify the configuration.
- Click Save.
Mappings
:
User Attributes
Set Target Object Actions to Create
and Update
(start with Delete
disabled for safety):
| LangSmith App Attribute | Microsoft Entra ID Attribute | Matching Precedence |
|---|---|---|
userName | userPrincipalName | |
active | Not([IsSoftDeleted]) | |
emails[type eq "work"].value | mail 1 | |
name.formatted | displayName OR Join(" ", [givenName], [surname]) 2 | |
externalId | objectId 3 | 1 |
- User’s email address must be present in Entra ID.
- Use the
Join
expression if yourdisplayName
does not match the format ofFirstname Lastname
. - To avoid inconsistency, this should match the SAML NameID assertion and the
sub
OAuth2.0 claim. For SAML SSO in cloud, theUnique User Identifier (Name ID)
required claim should beuser.objectID
and theName identifier format
should bepersistent
.
Create
and Update
only (start with Delete
disabled for safety):
| LangSmith App Attribute | Microsoft Entra ID Attribute | Matching Precedence |
|---|---|---|
displayName | displayName 1 | 1 |
externalId | objectId | |
members | members |
- Groups must follow the naming convention described in the Group Naming Convention section.
If your company has a group naming policy, you should instead map from the
description
Microsoft Entra ID Attribute and set the description based on the Group Naming Convention section.
- Under Applications > Applications, select your LangSmith Enterprise Application.
- Under the Assignments tab, click Assign then either Assign to People or Assign to Groups.
- Make the desired selection(s), then Assign and Done.
- Set Provisioning Status to
On
under Provisioning. - Monitor the initial sync to ensure users and groups are provisioned correctly.
- Once verified, enable
Delete
actions for both User and Group mappings.
Okta configuration steps
Supported features
- Create users
- Update user attributes
- Deactivate users
- Group push
- Import users
- Import groups
Step 1: Add application from Okta Integration Network
If you have already configured SSO login via SAML (cloud) or OAuth2.0 with OIDC (self-hosted), skip this step.
- In the General tab, ensure the
LangSmithUrl
is filled in according to the instructions from Step 1 - In the Provisioning tab, select
Integration
. - Select
Edit
thenEnable API integration
. - For API Token, paste the SCIM token you generated above.
- Keep
Import Groups
checked. - To verify the configuration, select Test API Credentials.
- Select Save.
- After saving the API integration details, new settings tabs appear on the left. Select
To App
. - Select Edit.
- Select the Enable checkbox for Create Users, Update Users, and Deactivate Users.
- Select Save.
- Assign users and/or groups in the Assignments tab. Assigned users are created and managed in your LangSmith group.
- Configure provisioning: under
Provisioning > To App > Provisioning to App
, clickEdit
, then checkCreate Users
,Update User Attributes
, andDeactivate Users
. - Under
<application_name> Attribute Mappings
, set the user attribute mappings as shown below, and delete the rest:
Follow Okta’s Enable Group Push instructions to configure groups to push by name or by rule.