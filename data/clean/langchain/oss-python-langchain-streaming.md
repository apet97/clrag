---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langchain-streaming",
  "h1": "oss-python-langchain-streaming",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.468645",
  "sha256_raw": "183693a9aafe2ddf9aa3d98f0843842e253614654a39a83d2b57ee537b4a3b35"
}
---

# oss-python-langchain-streaming

> Source: https://docs.langchain.com/oss/python/langchain/streaming

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Overview
LangChain’s streaming system lets you surface live feedback from agent runs to your application. What’s possible with LangChain streaming:- Stream agent progress — get state updates after each agent step.
- Stream LLM tokens — stream language model tokens as they’re generated.
- Stream custom updates — emit user-defined signals (e.g.,
"Fetched 10/100 records"
). - Stream multiple modes — choose from
updates
(agent progress),messages
(LLM tokens + metadata), orcustom
(arbitrary user data).
Agent progress
To stream agent progress, use thestream()
or astream()
methods with stream_mode="updates"
. This emits an event after every agent step.
For example, if you have an agent that calls a tool once, you should see the following updates:
- LLM node:
AIMessage
with tool call requests - Tool node:
ToolMessage
with execution result - LLM node: Final AI response
Streaming agent progress
Output
LLM tokens
To stream tokens as they are produced by the LLM, usestream_mode="messages"
. Below you can see the output of the agent streaming tool calls and the final response.
Streaming LLM tokens
Output
Custom updates
To stream updates from tools as they are executed, you can useget_stream_writer
.
Streaming custom updates
Output
Stream multiple modes
You can specify multiple streaming modes by passing stream mode as a list:stream_mode=["updates", "custom"]
:
Streaming multiple modes
Output