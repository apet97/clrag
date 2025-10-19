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