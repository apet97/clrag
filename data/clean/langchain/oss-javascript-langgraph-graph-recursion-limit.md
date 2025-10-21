---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langgraph-graph-recursion-limit",
  "h1": "oss-javascript-langgraph-graph-recursion-limit",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.476100",
  "sha256_raw": "d3d7bfadb58c294f3c459d0ee628f6c7371bca882ae2498b96b4382a49d7ec9c"
}
---

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