---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langgraph-streaming",
  "h1": "oss-python-langgraph-streaming",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.440509",
  "sha256_raw": "c777a2e75fe32eadca7c780c76d54841d06a517537ed31f325205b1f06b3da74"
}
---

# oss-python-langgraph-streaming

> Source: https://docs.langchain.com/oss/python/langgraph/streaming

- Stream graph state — get state updates / values with
updates
andvalues
modes. - Stream subgraph outputs — include outputs from both the parent graph and any nested subgraphs.
- Stream LLM tokens — capture token streams from anywhere: inside nodes, subgraphs, or tools.
- Stream custom data — send custom updates or progress signals directly from tool functions.
- Use multiple streaming modes — choose from
values
(full state),updates
(state deltas),messages
(LLM tokens + metadata),custom
(arbitrary user data), ordebug
(detailed traces).
Supported stream modes
Pass one or more of the following stream modes as a list to thestream()
or astream()
methods:
| Mode | Description |
|---|---|
values | Streams the full value of the state after each step of the graph. |
updates | Streams the updates to the state after each step of the graph. If multiple updates are made in the same step (e.g., multiple nodes are run), those updates are streamed separately. |
custom | Streams custom data from inside your graph nodes. |
messages | Streams 2-tuples (LLM token, metadata) from any graph nodes where an LLM is invoked. |
debug | Streams as much information as possible throughout the execution of the graph. |
Basic usage example
LangGraph graphs expose the.stream()
(sync) and .astream()
(async) methods to yield streamed outputs as iterators.
Extended example: streaming updates
Extended example: streaming updates
Stream multiple modes
You can pass a list as thestream_mode
parameter to stream multiple modes at once.
The streamed outputs will be tuples of (mode, chunk)
where mode
is the name of the stream mode and chunk
is the data streamed by that mode.
Stream graph state
Use the stream modesupdates
and values
to stream the state of the graph as it executes.
updates
streams the updates to the state after each step of the graph.values
streams the full value of the state after each step of the graph.
- updates
- values
Stream subgraph outputs
To include outputs from subgraphs in the streamed outputs, you can setsubgraphs=True
in the .stream()
method of the parent graph. This will stream outputs from both the parent graph and any subgraphs.
The outputs will be streamed as tuples (namespace, data)
, where namespace
is a tuple with the path to the node where a subgraph is invoked, e.g. ("parent_node:<task_id>", "child_node:<task_id>")
.
Extended example: streaming from subgraphs
Extended example: streaming from subgraphs
Debugging
Use thedebug
streaming mode to stream as much information as possible throughout the execution of the graph. The streamed outputs include the name of the node as well as the full state.
LLM tokens
Use themessages
streaming mode to stream Large Language Model (LLM) outputs token by token from any part of your graph, including nodes, tools, subgraphs, or tasks.
The streamed output from messages
mode is a tuple (message_chunk, metadata)
where:
message_chunk
: the token or message segment from the LLM.metadata
: a dictionary containing details about the graph node and LLM invocation.
If your LLM is not available as a LangChain integration, you can stream its outputs using custom
mode instead. See use with any LLM for details.
RunnableConfig
to ainvoke()
to enable proper streaming. See Async with Python < 3.11 for details or upgrade to Python 3.11+.Filter by LLM invocation
You can associatetags
with LLM invocations to filter the streamed tokens by LLM invocation.
Extended example: filtering by tags
Extended example: filtering by tags
Filter by node
To stream tokens only from specific nodes, usestream_mode="messages"
and filter the outputs by the langgraph_node
field in the streamed metadata:
Extended example: streaming LLM tokens from specific nodes
Extended example: streaming LLM tokens from specific nodes
Stream custom data
To send custom user-defined data from inside a LangGraph node or tool, follow these steps:- Use
get_stream_writer
to access the stream writer and emit custom data. - Set
stream_mode="custom"
when calling.stream()
or.astream()
to get the custom data in the stream. You can combine multiple modes (e.g.,["updates", "custom"]
), but at least one must be"custom"
.
get_stream_writer
in async for Python < 3.11
In async code running on Python < 3.11, get_stream_writer
will not work.
Instead, add a writer
parameter to your node or tool and pass it manually.
See Async with Python < 3.11 for usage examples.- node
- tool
Use with any LLM
You can usestream_mode="custom"
to stream data from any LLM API — even if that API does not implement the LangChain chat model interface.
This lets you integrate raw LLM clients or external services that provide their own streaming interfaces, making LangGraph highly flexible for custom setups.
Extended example: streaming arbitrary chat model
Extended example: streaming arbitrary chat model
Disable streaming for specific chat models
If your application mixes models that support streaming with those that do not, you may need to explicitly disable streaming for models that do not support it. Setdisable_streaming=True
when initializing the model.
- init_chat_model
- chat model interface
Async with Python < 3.11
In Python versions < 3.11, asyncio tasks do not support thecontext
parameter.
This limits LangGraph ability to automatically propagate context, and affects LangGraph’s streaming mechanisms in two key ways:
- You must explicitly pass
RunnableConfig
into async LLM calls (e.g.,ainvoke()
), as callbacks are not automatically propagated. - You cannot use
get_stream_writer
in async nodes or tools — you must pass awriter
argument directly.
Extended example: async LLM call with manual config
Extended example: async LLM call with manual config
Extended example: async custom streaming with stream writer
Extended example: async custom streaming with stream writer