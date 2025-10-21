---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langgraph-use-time-travel",
  "h1": "oss-python-langgraph-use-time-travel",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.436813",
  "sha256_raw": "3e27b905aa62d713515be95ec103b05b0ccdb0dac9460812be4d99cb2e26482c"
}
---

# oss-python-langgraph-use-time-travel

> Source: https://docs.langchain.com/oss/python/langgraph/use-time-travel

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
- Understand reasoning: Analyze the steps that led to a successful result.
- Debug mistakes: Identify where and why errors occurred.
- Explore alternatives: Test different paths to uncover better solutions.
- Run the graph with initial inputs using
invoke
orstream
methods. - Identify a checkpoint in an existing thread: Use the
get_state_history()
method to retrieve the execution history for a specificthread_id
and locate the desiredcheckpoint_id
. Alternatively, set an interrupt before the node(s) where you want execution to pause. You can then find the most recent checkpoint recorded up to that interrupt. - Update the graph state (optional): Use the
update_state
method to modify the graph’s state at the checkpoint and resume execution from alternative state. - Resume execution from the checkpoint: Use the
invoke
orstream
methods with an input ofNone
and a configuration containing the appropriatethread_id
andcheckpoint_id
.
In a workflow
This example builds a simple LangGraph workflow that generates a joke topic and writes a joke using an LLM. It demonstrates how to run the graph, retrieve past execution checkpoints, optionally modify the state, and resume execution from a chosen checkpoint to explore alternate outcomes.Setup
First we need to install the packages required1. Run the graph
2. Identify a checkpoint
3. Update the state
update_state
will create a new checkpoint. The new checkpoint will be associated with the same thread, but a new checkpoint ID.