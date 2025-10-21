---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-concepts-context",
  "h1": "oss-python-concepts-context",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.491066",
  "sha256_raw": "d753ea1007f815220fe563fd3f9ada7ceef011cada6fcd9e2ccff6b52f505718"
}
---

# oss-python-concepts-context

> Source: https://docs.langchain.com/oss/python/concepts/context

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
- By mutability:
- Static context: Immutable data that doesn’t change during execution (e.g., user metadata, database connections, tools)
- Dynamic context: Mutable data that evolves as the application runs (e.g., conversation history, intermediate results, tool call observations)
- By lifetime:
- Runtime context: Data scoped to a single run or invocation
- Cross-conversation context: Data that persists across multiple conversations or sessions
Runtime context refers to local context: data and dependencies your code needs to run. It does not refer to:
- The LLM context, which is the data passed into the LLM’s prompt.
- The “context window”, which is the maximum number of tokens that can be passed to the LLM.
| Context type | Description | Mutability | Lifetime | Access method |
|---|---|---|---|---|
| Static runtime context | User metadata, tools, db connections passed at startup | Static | Single run | context argument to invoke /stream |
| Dynamic runtime context (state) | Mutable data that evolves during a single run | Dynamic | Single run | LangGraph state object |
| Dynamic cross-conversation context (store) | Persistent data shared across conversations | Dynamic | Cross-conversation | LangGraph store |
Static runtime context
Static runtime context represents immutable data like user metadata, tools, and database connections that are passed to an application at the start of a run via thecontext
argument to invoke
/stream
. This data does not change during execution.
The
Runtime
object can be used to access static context and other utilities like the active store and stream writer.
See the [Runtime][langgraph.runtime.Runtime] documentation for details.Dynamic runtime context
Dynamic runtime context represents mutable data that can evolve during a single run and is managed through the LangGraph state object. This includes conversation history, intermediate results, and values derived from tools or LLM outputs. In LangGraph, the state object acts as short-term memory during a run.- In an agent
- In a workflow
Turning on memory
Please see the memory guide for more details on how to enable memory. This is a powerful feature that allows you to persist the agent’s state across multiple invocations. Otherwise, the state is scoped only to a single run.
Dynamic cross-conversation context
Dynamic cross-conversation context represents persistent, mutable data that spans across multiple conversations or sessions and is managed through the LangGraph store. This includes user profiles, preferences, and historical interactions. The LangGraph store acts as long-term memory across multiple runs. This can be used to read or update persistent facts (e.g., user profiles, preferences, prior interactions).See also
- Memory conceptual overview
- Short-term memory in LangChain
- Long-term memory in LangChain
- Memory in LangGraph