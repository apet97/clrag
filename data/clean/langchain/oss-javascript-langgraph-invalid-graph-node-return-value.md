---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langgraph-invalid-graph-node-return-value",
  "h1": "oss-javascript-langgraph-invalid-graph-node-return-value",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.447334",
  "sha256_raw": "e20f18762661be43955079c54711bc674a35e60ab21dc3c75bd56168a6407735"
}
---

# oss-javascript-langgraph-invalid-graph-node-return-value

> Source: https://docs.langchain.com/oss/javascript/langgraph/INVALID_GRAPH_NODE_RETURN_VALUE

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
StateGraph
received a non-object return type from a node. Here’s an example:
Troubleshooting
The following may help resolve this error:- If you have complex logic in your node, make sure all code paths return an appropriate object for your defined state.