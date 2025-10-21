---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langchain-runtime",
  "h1": "oss-python-langchain-runtime",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.492262",
  "sha256_raw": "670c4bf75823d91c78b9fc207512b16327eb28609fbd70ce106a99ed18a5232e"
}
---

# oss-python-langchain-runtime

> Source: https://docs.langchain.com/oss/python/langchain/runtime

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Overview
LangChain’screate_agent
runs on LangGraph’s runtime under the hood.
LangGraph exposes a Runtime object with the following information:
- Context: static information like user id, db connections, or other dependencies for an agent invocation
- Store: a BaseStore instance used for long-term memory
- Stream writer: an object used for streaming information via the
"custom"
stream mode
Access
When creating an agent withcreate_agent
, you can specify a context_schema
to define the structure of the context
stored in the agent Runtime.
When invoking the agent, pass the context
argument with the relevant configuration for the run:
Inside tools
You can access the runtime information inside tools to:- Access the context
- Read or write long-term memory
- Write to the custom stream (ex, tool progress / updates)
ToolRuntime
parameter to access the Runtime object inside a tool.
Inside middleware
You can access runtime information in middleware to create dynamic prompts, modify messages, or control agent behavior based on user context. Userequest.runtime
to access the Runtime object inside middleware decorators. The runtime object is available in the ModelRequest
parameter passed to middleware functions.