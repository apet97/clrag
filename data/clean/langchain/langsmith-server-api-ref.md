---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-server-api-ref",
  "h1": "langsmith-server-api-ref",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.450781",
  "sha256_raw": "0e8fb6ea7eb4e2a3b3208ab882b2ea1252b47c2270c79e1d20501c99c09fdecd"
}
---

# langsmith-server-api-ref

> Source: https://docs.langchain.com/langsmith/server-api-ref

/docs
endpoint (e.g. http://localhost:8124/docs
).
View the API reference.
Authentication
For deployments to LangSmith, authentication is required. Pass theX-Api-Key
header with each request to the LangGraph Server. The value of the header should be set to a valid LangSmith API key for the organization where the LangGraph Server is deployed.
Example curl
command: