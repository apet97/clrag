---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langchain-tools",
  "h1": "oss-javascript-langchain-tools",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.448136",
  "sha256_raw": "f0a0832ce60b777728e2b932ea223df2b2c42637d5f8930022697a0a4c93d0f3"
}
---

# oss-javascript-langchain-tools

> Source: https://docs.langchain.com/oss/javascript/langchain/tools

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Server-side tool useSome chat models (e.g., OpenAI, Anthropic, and Gemini) feature built-in tools that are executed server-side, such as web search and code interpreters. Refer to the provider overview to learn how to access these tools with your specific chat model.
Create tools
Basic tool definition
The simplest way to create a tool is by importing thetool
function from the langchain
package. You can use zod to define the tool’s input schema:
Accessing Context
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
annotations.Context
Access immutable configuration and contextual data like user IDs, session details, or application-specific configuration throughruntime.context
.
Tools can access an agent’s runtime context through the config
parameter:
Memory (Store)
Access persistent data across conversations using the store. The store is accessed viaruntime.store
and allows you to save and retrieve user-specific or application-specific data.
Stream Writer
Stream custom updates from tools as they execute usingruntime.stream_writer
. This is useful for providing real-time feedback to users about what a tool is doing.