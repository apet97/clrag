---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langgraph-graph-recursion-limit",
  "h1": "oss-python-langgraph-graph-recursion-limit",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.477326",
  "sha256_raw": "84858fd4e646ebf2ca130006fc1e9a86631bb5bf4392877a17600fe02084e257"
}
---

# oss-python-langgraph-graph-recursion-limit

> Source: https://docs.langchain.com/oss/python/langgraph/GRAPH_RECURSION_LIMIT

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
StateGraph
reached the maximum number of steps before hitting a stop condition.
This is often due to an infinite loop caused by code like the example below:
Troubleshooting
- If you are not expecting your graph to go through many iterations, you likely have a cycle. Check your logic for infinite loops.
-
If you have a complex graph, you can pass in a higher
recursion_limit
value into yourconfig
object when invoking your graph like this: