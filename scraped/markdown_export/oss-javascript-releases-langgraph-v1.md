# oss-javascript-releases-langgraph-v1

> Source: https://docs.langchain.com/oss/javascript/releases/langgraph-v1

createAgent
is built on LangGraph) so you can start high-level and drop down to granular control when needed.
Stable core APIs
Graph primitives (state, nodes, edges) and the execution/runtime model are unchanged, making upgrades straightforward.
Reliability, by default
Durable execution with checkpointing, persistence, streaming, and human-in-the-loop continues to be first-class.
Seamless with LangChain v1
LangChain’s
createAgent
runs on LangGraph. Use LangChain for a fast start; drop to LangGraph for custom orchestration.Deprecation of createReactAgent
The LangGraph createReactAgent
prebuilt has been deprecated in favor of LangChain’s createAgent
. It provides a simpler interface, and offers greater customization potential through the introduction of middleware.
- For information on the new
createAgent
API, see the LangChain v1 release notes. - For information on migrating from
createReactAgent
tocreateAgent
, see the LangChain v1 migration guide.
Typed interrupts
StateGraph
now accepts a map of interrupt types in the constructor to more closely constrain the types of interrupts that can be used within a graph.
Frontend SDK enhancements
LangGraph v1 comes with a few enhancements when interacting with a LangGraph application from the frontend.Event stream encoding
The low-leveltoLangGraphEventStream
helper has been removed. Streaming responses are now handled natively by the SDK, and you can select the wire format via passing in the encoding
format to graph.stream
. This makes switching between SSE and normal JSON responses straightforward without changing UI logic.
See the migration guide for more information.
Custom transports in useStream
The React useStream
hook now supports pluggable transports so you can have more control over the network layer without changing UI code.
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