---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-openapi-security",
  "h1": "langsmith-openapi-security",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.433545",
  "sha256_raw": "d53f481881b55c0116748a61130aee7e8bc5edc9de7be119b767c72b03a21adf"
}
---

# langsmith-openapi-security

> Source: https://docs.langchain.com/langsmith/openapi-security

This guide applies to all LangSmith deployments (Cloud and self-hosted). It does not apply to usage of the LangGraph open source library if you are not using LangSmith.
Default Schema
The default security scheme varies by deployment type:- LangSmith
x-api-key
header:
- Self-hosted
Custom Security Schema
To customize the security schema in your OpenAPI documentation, add anopenapi
field to your auth
configuration in langgraph.json
. Remember that this only updates the API documentation - you must also implement the corresponding authentication logic as shown in How to add custom authentication.
Note that LangSmith does not provide authentication endpoints - you’ll need to handle user authentication in your client application and pass the resulting credentials to the LangGraph API.
- OAuth2 with Bearer Token
- API Key
Testing
After updating your configuration:- Deploy your application
- Visit
/docs
to see the updated OpenAPI documentation - Try out the endpoints using credentials from your authentication server (make sure you’ve implemented the authentication logic first)