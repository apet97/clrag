---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langgraph-invalid-concurrent-graph-update",
  "h1": "oss-javascript-langgraph-invalid-concurrent-graph-update",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.485740",
  "sha256_raw": "a12d4d132a049e00322eca6cbb721d5143f29e7dd76615f14737b1d290338edd"
}
---

# oss-javascript-langgraph-invalid-concurrent-graph-update

> Source: https://docs.langchain.com/oss/javascript/langgraph/INVALID_CONCURRENT_GRAPH_UPDATE

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
StateGraph
received concurrent updates to its state from multiple nodes to a state property that doesn’t
support it.
One way this can occur is if you are using a fanout
or other parallel execution in your graph and you have defined a graph like this:
{ someKey: "some_string_value" }
, this will overwrite the state value for someKey
with "some_string_value"
.
However, if multiple nodes in e.g. a fanout within a single step return values for someKey
, the graph will throw this error because
there is uncertainty around how to update the internal state.
To get around this, you can define a reducer that combines multiple values:
Troubleshooting
The following may help resolve this error:- If your graph executes nodes in parallel, make sure you have defined relevant state keys with a reducer.