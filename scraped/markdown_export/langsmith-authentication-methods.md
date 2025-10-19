# langsmith-authentication-methods

> Source: https://docs.langchain.com/langsmith/authentication-methods

Cloud
Email/Password
Users can use an email address and password to sign up and login to LangSmith.Social Providers
Users can alternatively use their credentials from GitHub or Google.SAML SSO
Enterprise customers can configure SAML SSO and SCIMSelf-Hosted
Self-hosted customers have more control over how their users can login to LangSmith. For more in-depth coverage of configuration options, see the self-hosting docs and Helm chart.SSO with OAuth 2.0 and OIDC
Production installations should configure SSO in order to use an external identity provider. This enables users to login through an identity platform like Auth0/Okta. LangSmith supports almost any OIDC-compliant provider. Learn more about configuring SSO in the SSO configuration guideEmail/Password a.k.a. basic auth
This auth method requires very little configuration as it does not require an external identity provider. It is most appropriate to use for self-hosted trials. Learn more in the basic auth configuration guideNone
This authentication mode will be removed after the launch of Basic Auth.