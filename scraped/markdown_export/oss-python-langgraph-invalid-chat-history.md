# oss-python-langgraph-invalid-chat-history

> Source: https://docs.langchain.com/oss/python/langgraph/INVALID_CHAT_HISTORY

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
call_model
graph node receives a malformed list of messages. Specifically, it is malformed when there are AIMessages
with tool_calls
(LLM requesting to call a tool) that do not have a corresponding ToolMessage
(result of a tool invocation to return to the LLM).
There could be a few reasons you’re seeing this error:
- You manually passed a malformed list of messages when invoking the graph, e.g.
graph.invoke({'messages': [AIMessage(..., tool_calls=[...])]})
- The graph was interrupted before receiving updates from the
tools
node (i.e. a list ofToolMessage
) and you invoked it with an input that is not None or a ToolMessage, e.g.graph.invoke({'messages': [HumanMessage(...)]}, config)
. This interrupt could have been triggered in one of the following ways:- You manually set
interrupt_before = ['tools']
increate_agent
- You manually set
- One of the tools raised an error that wasn’t handled by the ToolNode (
"tools"
)
Troubleshooting
To resolve this, you can do one of the following:- Don’t invoke the graph with a malformed list of messages
- In case of an interrupt (manual or due to an error) you can:
- provide
ToolMessage
objects that match existing tool calls and callgraph.invoke({'messages': [ToolMessage(...)]})
. NOTE: this will append the messages to the history and run the graph from the START node.- manually update the state and resume the graph from the interrupt:
- get the list of most recent messages from the graph state with
graph.get_state(config)
- modify the list of messages to either remove unanswered tool calls from AIMessages
- get the list of most recent messages from the graph state with
- manually update the state and resume the graph from the interrupt:
ToolMessage
objects with tool_call_ids
that match unanswered tool calls 3. call graph.update_state(config, {'messages': ...})
with the modified list of messages 4. resume the graph, e.g. call graph.invoke(None, config)