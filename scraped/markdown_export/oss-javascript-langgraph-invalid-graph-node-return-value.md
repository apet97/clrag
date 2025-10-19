# oss-javascript-langgraph-invalid-graph-node-return-value

> Source: https://docs.langchain.com/oss/javascript/langgraph/INVALID_GRAPH_NODE_RETURN_VALUE

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
StateGraph
received a non-object return type from a node. Here’s an example:
Troubleshooting
The following may help resolve this error:- If you have complex logic in your node, make sure all code paths return an appropriate object for your defined state.