---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langgraph-missing-checkpointer",
  "h1": "oss-javascript-langgraph-missing-checkpointer",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.447460",
  "sha256_raw": "d534419ff46f597ece86fb67e47e1bc1637b4cd0aabcbadf9456b0c8b4b4311a"
}
---

# oss-javascript-langgraph-missing-checkpointer

> Source: https://docs.langchain.com/oss/javascript/langgraph/MISSING_CHECKPOINTER

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
checkpointer
is missing in the compile()
method of StateGraph
or entrypoint
.
Troubleshooting
The following may help resolve this error:- Initialize and pass a checkpointer to the
compile()
method ofStateGraph
orentrypoint
.
- Use the LangGraph API so you don’t need to implement or configure checkpointers manually. The API handles all persistence infrastructure for you.
Related
- Read more about persistence.