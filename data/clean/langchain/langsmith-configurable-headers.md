---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-configurable-headers",
  "h1": "langsmith-configurable-headers",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.478624",
  "sha256_raw": "236e921fa18b6d6908774e2729203f83ce09c43f90a7326057732e8e79d54361"
}
---

# langsmith-configurable-headers

> Source: https://docs.langchain.com/langsmith/configurable-headers

LangGraph allows runtime configuration to modify agent behavior and permissions dynamically. When using LangSmith Deployment, you can pass this configuration in the request body (config) or specific request headers. This enables adjustments based on user identity or other requests.For privacy, control which headers are passed to the runtime configuration via the http.configurable_headers section in your langgraph.json file.Here’s how to customize the included and excluded headers:
The include and exclude lists accept exact header names or patterns using * to match any number of characters. For your security, no other regex patterns are supported.