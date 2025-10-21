---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langgraph-invalid-graph-node-return-value",
  "h1": "oss-python-langgraph-invalid-graph-node-return-value",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.479157",
  "sha256_raw": "c5efafd1b42a20ac010a1637b7754e3bfa5a0792d6c330f674998ebf9880d928"
}
---

# oss-python-langgraph-invalid-graph-node-return-value

> Source: https://docs.langchain.com/oss/python/langgraph/INVALID_GRAPH_NODE_RETURN_VALUE

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
StateGraph
received a non-dict return type from a node. Here’s an example:
Troubleshooting
The following may help resolve this error:- If you have complex logic in your node, make sure all code paths return an appropriate dict for your defined state.