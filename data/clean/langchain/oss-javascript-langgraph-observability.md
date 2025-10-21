---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langgraph-observability",
  "h1": "oss-javascript-langgraph-observability",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.484314",
  "sha256_raw": "f0539c75369d6b52a47e49c69e4ebbc83d02896ad799dd42d4e6e0f23cdebb0b"
}
---

# oss-javascript-langgraph-observability

> Source: https://docs.langchain.com/oss/javascript/langgraph/observability

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Prerequisites
Before you begin, ensure you have the following:- A LangSmith account (free to sign up)
Enable tracing
To enable tracing for your application, set the following environment variables:default
. To configure a custom project name, see Log to a project.
For more information, see Trace with LangGraph.
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
Use anonymizers to prevent logging of sensitive data in traces
You may want to mask sensitive data to prevent it from being logged to LangSmith. You can create anonymizers and apply them to your graph using configuration. This example will redact anything matching the Social Security Number format XXX-XX-XXXX from traces sent to LangSmith.TypeScript