---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-graph-rebuild",
  "h1": "langsmith-graph-rebuild",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.441483",
  "sha256_raw": "df30f60c990cdb781e3d78991f66f0dc289545498a8e74a9c28a55c97358b784"
}
---

# langsmith-graph-rebuild

> Source: https://docs.langchain.com/langsmith/graph-rebuild

Note
In most cases, customizing behavior based on the config should be handled by a single graph where each node can read a config and change its behavior based on it
Prerequisites
Make sure to check out this how-to guide on setting up your app for deployment first.Define graphs
Let’s say you have an app with a simple graph that calls an LLM and returns the response to the user. The app file directory looks like the following:openai_agent.py
.
No rebuild
In the standard LangGraph API configuration, the server uses the compiled graph instance that’s defined at the top level ofopenai_agent.py
, which looks like the following:
CompiledStateGraph
instance in your LangGraph API configuration (langgraph.json
), e.g.:
Rebuild
To make your graph rebuild on each new run with custom configuration, you need to rewriteopenai_agent.py
to instead provide a function that takes a config and returns a graph (or compiled graph) instance. Let’s say we want to return our existing graph for user ID ‘1’, and a tool-calling agent for other users. We can modify openai_agent.py
as follows:
make_graph
) in langgraph.json
: