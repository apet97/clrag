---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langchain-tools",
  "h1": "oss-python-langchain-tools",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.461547",
  "sha256_raw": "757c33184c8932d3bec38c538bc858ab096b0a20bf48e5d5c62ef8dd5b4dd5ef"
}
---

# oss-python-langchain-tools

> Source: https://docs.langchain.com/oss/python/langchain/tools

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Server-side tool useSome chat models (e.g., OpenAI, Anthropic, and Gemini) feature built-in tools that are executed server-side, such as web search and code interpreters. Refer to the provider overview to learn how to access these tools with your specific chat model.
Create tools
Basic tool definition
The simplest way to create a tool is with the@tool
decorator. By default, the function’s docstring becomes the tool’s description that helps the model understand when to use it:
Customize tool properties
Custom tool name
By default, the tool name comes from the function name. Override it when you need something more descriptive:Custom tool description
Override the auto-generated tool description for clearer model guidance:Advanced schema definition
Define complex inputs with Pydantic models or JSON schemas:Accessing Context
Why this matters: Tools are most powerful when they can access agent state, runtime context, and long-term memory. This enables tools to make context-aware decisions, personalize responses, and maintain information across conversations.
ToolRuntime
parameter, which provides:
- State - Mutable data that flows through execution (messages, counters, custom fields)
- Context - Immutable configuration like user IDs, session details, or application-specific configuration
- Store - Persistent long-term memory across conversations
- Stream Writer - Stream custom updates as tools execute
- Config - RunnableConfig for the execution
- Tool Call ID - ID of the current tool call
ToolRuntime
UseToolRuntime
to access all runtime information in a single parameter. Simply add runtime: ToolRuntime
to your tool signature, and it will be automatically injected without being exposed to the LLM.
ToolRuntime
: A unified parameter that provides tools access to state, context, store, streaming, config, and tool call ID. This replaces the older pattern of using separate InjectedState
, InjectedStore
, get_runtime()
, and InjectedToolCallId
annotations.ToolRuntime
:
The
tool_runtime
parameter is hidden from the model. For the example above, the model only sees pref_name
in the tool schema - tool_runtime
is not included in the request.Command
to update the agent’s state or control the graph’s execution flow:
Context
Access immutable configuration and contextual data like user IDs, session details, or application-specific configuration throughruntime.context
.
Tools can access runtime context through ToolRuntime
:
Memory (Store)
Access persistent data across conversations using the store. The store is accessed viaruntime.store
and allows you to save and retrieve user-specific or application-specific data.
Tools can access and update the store through ToolRuntime
:
Stream Writer
Stream custom updates from tools as they execute usingruntime.stream_writer
. This is useful for providing real-time feedback to users about what a tool is doing.