# langsmith-configurable-headers

> Source: https://docs.langchain.com/langsmith/configurable-headers

LangGraph allows runtime configuration to modify agent behavior and permissions dynamically. When using LangSmith Deployment, you can pass this configuration in the request body (config) or specific request headers. This enables adjustments based on user identity or other requests.For privacy, control which headers are passed to the runtime configuration via the http.configurable_headers section in your langgraph.json file.Here’s how to customize the included and excluded headers:
The include and exclude lists accept exact header names or patterns using * to match any number of characters. For your security, no other regex patterns are supported.