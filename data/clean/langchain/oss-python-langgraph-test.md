---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langgraph-test",
  "h1": "oss-python-langgraph-test",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.475697",
  "sha256_raw": "6280312c978f2e327dba9e5c869328016ead7b7228a4c9777be7cf267fbf7c0c"
}
---

# oss-python-langgraph-test

> Source: https://docs.langchain.com/oss/python/langgraph/test

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
create_agent
instead.
Prerequisites
First, make sure you havepytest
installed:
Getting started
Because many LangGraph agents depend on state, a useful pattern is to create your graph before each test where you use it, then compile it within tests with a new checkpointer instance. The below example shows how this works with a simple, linear graph that progresses throughnode1
and node2
. Each node updates the single state key my_key
:
Testing individual nodes and edges
Compiled LangGraph agents expose references to each individual node asgraph.nodes
. You can take advantage of this to test individual nodes within your agent. Note that this will bypass any checkpointers passed when compiling the graph:
Partial execution
For agents made up of larger graphs, you may wish to test partial execution paths within your agent rather than the entire flow end-to-end. In some cases, it may make semantic sense to restructure these sections as subgraphs, which you can invoke in isolation as normal. However, if you do not wish to make changes to your agent graph’s overall structure, you can use LangGraph’s persistence mechanisms to simulate a state where your agent is paused right before the beginning of the desired section, and will pause again at the end of the desired section. The steps are as follows:- Compile your agent with a checkpointer (the in-memory checkpointer
InMemorySaver
will suffice for testing). - Call your agent’s
update_state
method with anas_node
parameter set to the name of the node before the one you want to start your test. - Invoke your agent with the same
thread_id
you used to update the state and aninterrupt_after
parameter set to the name of the node you want to stop at.