# oss-javascript-concepts-context

> Source: https://docs.langchain.com/oss/javascript/concepts/context

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
| Context type | Description | Mutability | Lifetime |
|---|---|---|---|
| Config | data passed at the start of a run | Static | Single run |
| Dynamic runtime context (state) | Mutable data that evolves during a single run | Dynamic | Single run |
| Dynamic cross-conversation context (store) | Persistent data shared across conversations | Dynamic | Cross-conversation |
Config
Config is for immutable data like user metadata or API keys. Use this when you have values that don’t change mid-run. Specify configuration using a key called “configurable” which is reserved for this purpose.Dynamic runtime context
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