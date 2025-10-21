---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langchain-observability",
  "h1": "oss-python-langchain-observability",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.488781",
  "sha256_raw": "059cb4b086e8d0da566f1362052ac538d7331a4d34dcfc8fd74b7b94e11a3596"
}
---

# oss-python-langchain-observability

> Source: https://docs.langchain.com/oss/python/langchain/observability

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
create_agent
, you get built-in observability through LangSmith - a powerful platform for tracing, debugging, evaluating, and monitoring your LLM applications.
Traces capture every step your agent takes, from the initial user input to the final response, including all tool calls, model interactions, and decision points. This enables you to debug your agents, evaluate performance, and monitor usage.
Prerequisites
Before you begin, ensure you have the following:- A LangSmith account (free to sign up)
Enable tracing
All LangChain agents automatically support LangSmith tracing. To enable it, set the following environment variables:Quick start
No extra code is needed to log a trace to LangSmith. Just run your agent code as you normally would:default
. To configure a custom project name, see Log to a project.
Trace selectively
You may opt to trace specific invocations or parts of your application using LangSmith’stracing_context
context manager:
Log to a project
Statically
Statically
You can set a custom project name for your entire application by setting the
LANGSMITH_PROJECT
environment variable:Dynamically
Dynamically
You can set the project name programmatically for specific operations:
Add metadata to traces
You can annotate your traces with custom metadata and tags:tracing_context
also accepts tags and metadata for fine-grained control: