---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langgraph-multiple-subgraphs",
  "h1": "oss-javascript-langgraph-multiple-subgraphs",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.458540",
  "sha256_raw": "ba67ea0008b8a0ee5207b51e125a58aea80613bc1ccf4a49043f7641bcafdcdf"
}
---

# oss-javascript-langgraph-multiple-subgraphs

> Source: https://docs.langchain.com/oss/javascript/langgraph/MULTIPLE_SUBGRAPHS

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Troubleshooting
The following may help resolve this error:-
If you don’t need to interrupt/resume from a subgraph, pass
checkpointer: false
when compiling it like this:.compile({ checkpointer: false })
-
Don’t imperatively call graphs multiple times in the same node, and instead use the
Send
API.