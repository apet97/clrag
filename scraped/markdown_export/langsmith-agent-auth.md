# langsmith-agent-auth

> Source: https://docs.langchain.com/langsmith/agent-auth

Installation
Install the Agent Auth client library from PyPI:Quickstart
1. Initialize the client
2. Set up OAuth providers
Before agents can authenticate, you need to configure an OAuth provider using the following process:- Select a unique identifier for your OAuth provider to use in LangChain’s platform (e.g., “github-local-dev”, “google-workspace-prod”).
- Go to your OAuth provider’s developer console and create a new OAuth application.
-
Set LangChain’s API as an available callback URL using this structure:
For example, if your provider_id is “github-local-dev”, use:
-
Use
client.create_oauth_provider()
with the credentials from your OAuth app:
3. Authenticate from an agent
The clientauthenticate()
API is used to get OAuth tokens from pre-configured providers. On the first call, it takes the caller through an OAuth 2.0 auth flow.
In LangGraph context
By default, tokens are scoped to the calling agent using the Assistant ID parameter.Outside LangGraph context
Provide theauth_url
to the user for out-of-band OAuth flows.