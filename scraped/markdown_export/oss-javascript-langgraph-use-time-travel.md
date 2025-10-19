# oss-javascript-langgraph-use-time-travel

> Source: https://docs.langchain.com/oss/javascript/langgraph/use-time-travel

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
- Understand reasoning: Analyze the steps that led to a successful result.
- Debug mistakes: Identify where and why errors occurred.
- Explore alternatives: Test different paths to uncover better solutions.
- Run the graph with initial inputs using
invoke
orstream
methods. - Identify a checkpoint in an existing thread: Use the
getStateHistory()
method to retrieve the execution history for a specificthread_id
and locate the desiredcheckpoint_id
. Alternatively, set a breakpoint before the node(s) where you want execution to pause. You can then find the most recent checkpoint recorded up to that breakpoint. - Update the graph state (optional): Use the
updateState
method to modify the graph’s state at the checkpoint and resume execution from alternative state. - Resume execution from the checkpoint: Use the
invoke
orstream
methods with an input ofnull
and a configuration containing the appropriatethread_id
andcheckpoint_id
.
In a workflow
This example builds a simple LangGraph workflow that generates a joke topic and writes a joke using an LLM. It demonstrates how to run the graph, retrieve past execution checkpoints, optionally modify the state, and resume execution from a chosen checkpoint to explore alternate outcomes.Setup
First we need to install the packages required1. Run the graph
2. Identify a checkpoint
3. Update the state
updateState
will create a new checkpoint. The new checkpoint will be associated with the same thread, but a new checkpoint ID.