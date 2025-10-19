# oss-javascript-langchain-runtime

> Source: https://docs.langchain.com/oss/javascript/langchain/runtime

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Overview
LangChain’screateAgent
runs on LangGraph’s runtime under the hood.
LangGraph exposes a Runtime object with the following information:
- Context: static information like user id, db connections, or other dependencies for an agent invocation
- Store: a BaseStore instance used for long-term memory
- Stream writer: an object used for streaming information via the
"custom"
stream mode
Access
When creating an agent withcreateAgent
, you can specify a contextSchema
to define the structure of the context
stored in the agent Runtime.
When invoking the agent, pass the context
argument with the relevant configuration for the run:
Inside tools
You can access the runtime information inside tools to:- Access the context
- Read or write long-term memory
- Write to the custom stream (ex, tool progress / updates)
runtime
parameter to access the Runtime object inside a tool.
Inside middleware
You can access runtime information in middleware to create dynamic prompts, modify messages, or control agent behavior based on user context. Use theruntime
parameter to access the Runtime object inside middleware.