# oss-python-releases-langgraph-v1

> Source: https://docs.langchain.com/oss/python/releases/langgraph-v1

create_agent
is built on LangGraph) so you can start high-level and drop down to granular control when needed.
Stable core APIs
Graph primitives (state, nodes, edges) and the execution/runtime model are unchanged, making upgrades straightforward.
Reliability, by default
Durable execution with checkpointing, persistence, streaming, and human-in-the-loop continues to be first-class.
Seamless with LangChain v1
LangChain’s
create_agent
runs on LangGraph. Use LangChain for a fast start; drop to LangGraph for custom orchestration.Deprecation of create_react_agent
The LangGraph create_react_agent
prebuilt has been deprecated in favor of LangChain’s create_agent
. It provides a simpler interface, and offers greater customization potential through the introduction of middleware.
- For information on the new
create_agent
API, see the LangChain v1 release notes. - For information on migrating from
create_react_agent
tocreate_agent
, see the LangChain v1 migration guide.
Reporting issues
Please report any issues discovered with 1.0 on GitHub using the'v1'
label.
Additional resources
LangGraph 1.0
Read the announcement
Overview
What LangGraph is and when to use it
Graph API
Build graphs with state, nodes, and edges
LangChain Agents
High-level agents built on LangGraph
Migration guide
How to migrate to LangGraph v1
GitHub
Report issues or contribute
See also
- Versioning - Understanding version numbers
- Release policy - Detailed release policies