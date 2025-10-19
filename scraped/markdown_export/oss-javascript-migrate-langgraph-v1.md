# oss-javascript-migrate-langgraph-v1

> Source: https://docs.langchain.com/oss/javascript/migrate/langgraph-v1

Summary of changes
| Area | What changed |
|---|---|
| React prebuilt | createReactAgent deprecated; use LangChain createAgent |
| Interrupts | Typed interrupts supported via interrupts config |
toLangGraphEventStream removed | Use graph.stream with the desired encoding format |
useStream | Supports custom transports |
Deprecation: createReactAgent
→ createAgent
LangGraph v1 deprecates the createReactAgent
prebuilt. Use LangChain’s createAgent
, which runs on LangGraph and adds a flexible middleware system.
See the LangChain v1 docs for details:
Typed interrupts
You can now define interrupt types at graph construction to strictly type the values passed to and received from interrupts.Event stream encoding
The low-leveltoLangGraphEventStream
helper is removed. Streaming responses are handled by the SDK; when using low-level clients, select the wire format via an encoding
option passed to graph.stream
.
Breaking changes
Dropped Node 18 support
All LangGraph packages now require Node.js 20 or higher. Node.js 18 reached end of life in March 2025.New build outputs
Builds for all langgraph packages now use a bundler based approach instead of using raw typescript outputs. If you were importing files from thedist/
directory (which is not recommended), you will need to update your imports to use the new module system.