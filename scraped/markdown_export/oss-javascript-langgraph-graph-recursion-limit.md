# oss-javascript-langgraph-graph-recursion-limit

> Source: https://docs.langchain.com/oss/javascript/langgraph/GRAPH_RECURSION_LIMIT

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
StateGraph
reached the maximum number of steps before hitting a stop condition.
This is often due to an infinite loop caused by code like the example below:
Troubleshooting
- If you are not expecting your graph to go through many iterations, you likely have a cycle. Check your logic for infinite loops.
-
If you have a complex graph, you can pass in a higher
recursionLimit
value into yourconfig
object when invoking your graph like this: