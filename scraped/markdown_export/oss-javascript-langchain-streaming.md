# oss-javascript-langchain-streaming

> Source: https://docs.langchain.com/oss/javascript/langchain/streaming

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
method with streamMode: "updates"
. This emits an event after every agent step.
For example, if you have an agent that calls a tool once, you should see the following updates:
- LLM node:
AIMessage
with tool call requests - Tool node: @[
ToolMessage
] with execution result - LLM node: Final AI response
LLM tokens
To stream tokens as they are produced by the LLM, usestreamMode: "messages"
:
Custom updates
To stream updates from tools as they are executed, you can use thewriter
parameter from the configuration.
Output
If you add the
writer
parameter to your tool, you won’t be able to invoke the tool outside of a LangGraph execution context without providing a writer function.Stream multiple modes
You can specify multiple streaming modes by passing streamMode as an array:streamMode: ["updates", "messages", "custom"]
: