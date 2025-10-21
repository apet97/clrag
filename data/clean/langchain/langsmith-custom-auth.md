---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-custom-auth",
  "h1": "langsmith-custom-auth",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.462542",
  "sha256_raw": "0d168e3ed69a58168296de22319eaa12b8cc7a14b13e222f63fca3de55a20256"
}
---

# langsmith-custom-auth

> Source: https://docs.langchain.com/langsmith/custom-auth

Add custom authentication to your deployment
To leverage custom authentication and access user-level metadata in your deployments, set up custom authentication to automatically populate theconfig["configurable"]["langgraph_auth_user"]
object through a custom authentication handler. You can then access this object in your graph with the langgraph_auth_user
key to allow an agent to perform authenticated actions on behalf of the user.
-
Implement authentication:
Without a custom
@auth.authenticate
handler, LangGraph sees only the API-key owner (usually the developer), so requests aren’t scoped to individual end-users. To propagate custom tokens, you must implement your own handler.
- This handler receives the request (headers, etc.), validates the user, and returns a dictionary with at least an identity field.
- You can add any custom fields you want (e.g., OAuth tokens, roles, org IDs, etc.).
-
In your
langgraph.json
, add the path to your auth file: -
Once you’ve set up authentication in your server, requests must include the required authorization information based on your chosen scheme. Assuming you are using JWT token authentication, you could access your deployments using any of the following methods:
For more details on RemoteGraph, refer to the Use RemoteGraph guide.
- Python Client
- Python RemoteGraph
- JavaScript Client
- JavaScript RemoteGraph
- CURL
Enable agent authentication
After authentication, the platform creates a special configuration object (config
) that is passed to LangSmith deployment. This object contains information about the current user, including any custom fields you return from your @auth.authenticate
handler.
To allow an agent to perform authenticated actions on behalf of the user, access this object in your graph with the langgraph_auth_user
key:
Fetch user credentials from a secure secret store. Storing secrets in graph state is not recommended.
Authorizing a user for Studio
By default, if you add custom authorization on your resources, this will also apply to interactions made from Studio. If you want, you can handle logged-in Studio users differently by checking is_studio_user().is_studio_user
was added in version 0.1.73 of the langgraph-sdk. If you’re on an older version, you can still check whether isinstance(ctx.user, StudioUser)
.