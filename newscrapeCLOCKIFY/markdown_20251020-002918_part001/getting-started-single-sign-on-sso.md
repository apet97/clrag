# getting-started-single-sign-on-sso

> Source: https://clockify.me/help/getting-started/single-sign-on-sso

Single sign-on (SSO)
Single sign-on feature (hereafter SSO) provides security at scale by controlling access and managing login credentials while using your company’s IdP via both SAML 2.0 and OAuth 2.0 (OIDC) (Office 365, Okta, Azure, Active Directory, Google, OneLogin…).
This is a paid feature, which you can enable by upgrading your workspace to Enterprise plan.
In order to use SSO, you first need to move your workspace to subdomain. Once you do that, you can configure SSO settings and disable other login methods.
Setting up custom subdomain #
Moving to subdomain #
Before you can configure and start using SSO for authorization, you need to move your Clockify app domain to a custom subdomain.
When you upgrade your Clockify subscription to Enterprise plan, you will get Authentication tab in the Workspace settings. There, you can enter the subdomain you’d like to use and move your workspace there.
To set up subdomain:
- Navigate to the Authentication tab in the Workspace settings
- Enter your custom subdomain in the provided field
- Click Create subdomain and Create to confirm the action
After you created your subdomain and moved your workspace there, Google login will no longer work for you and your users.
If you’d, however, like to use Google login, you need to set it up manually by configuring OAuth 2.0 (OIDC) for SSO.
For more information, check out the OAuth 2.0 (OIDC) with Google section below.
Accessing Clockify from subdomain #
After you create your subdomain, you’ll automatically be logged out of any apps you were logged in with your Clockify account. You’ll have access to them only through the subdomain you created (e.g. https://yourcompanysubdomain.clockify.me/login).
Workspaces on subdomain #
Subdomain is tied to only one workspace. Users on subdomain can’t have multiple workspaces: there is no workspace switcher, no workspaces in the sidebar, and no access to subdomain workspace from the main domain.
To access multiple workspaces, log in to the main Clockify domain.
Changing subdomain #
You can change subdomain URL at any time.
Once you change your URL, your Users will be logged out and will have to use the workspace through the new URL.
If you cancel the subscription to the Enterprise plan:
- you’ll move back to the main domain when the subscription expires
- your subdomain will become available for others to use
- your users will have to log in with their email
API keys on subdomain #
For security reasons, each user on subdomain gets a separate API key that works only for that workspace – meaning, no one can access your data on your subdomain unless they have the right authorization.
If, for example, there is a user with two separate Enterprise workspaces, workspace owners can’t see, or access data from each others accounts.
Inviting new users #
Once you’re in the subdomain workspace, you can invite users one by one using email (like before), or let anyone join without you having to manually invite them.
To let anyone join, check the Users can join without an invite checkbox.
If you use SSO and someone without an account tries to log in, the account will be automatically created for them and they’ll log in.
If you allow Log in with email, people will be able to create an account and automatically join your workspace.
Configuring SSO #
If you’d like to use SSO via your mobile devices (android or iOS) all the SSO configurations supported by Clockify should contain [yourcompany subdomain].clockify.me links. For example, in the Redirect URL section add https://yourcompanysubdomain.clockify.me/login/android/oauth2 or https://yourcompanysubdomain.clockify.me/login/ios/oauth2 link.
Clockify supports all major SSO identity providers:
- SAML 2.0 (Google, OneLogin, Okta, Azure, Rippling, JumpCloud)
- OAuth 2.0 (OIDC) (Google, Azure, Okta)
Only workspace owner can see Authorization tab, manage subdomain, configure SSO, and turn SSO on/off.
If you wish to force everyone to log in with SSO, simply turn off the Log in with email option. Once this change has been saved, your workspace members accounts will be required to use SSO to log in.
Data in the SSO configuration can always be edited or deleted. If deleted, your users will have to switch back to logging in by using email.
Owner can always log in using the original credentials at https://mysubdomain.clockify.me/login-owner
To add Default Relay State, use the parameters below.
Make sure to use curly brackets and straight quotes instead of the curly ones, otherwise it won’t work.
Example of Default Relay State:
{"location":"https://yourcompanysubdomain.clockify.me", "organizationName":"yourcompanysubdomain"}