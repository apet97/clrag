# oss-python-langgraph-missing-checkpointer

> Source: https://docs.langchain.com/oss/python/langgraph/MISSING_CHECKPOINTER

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