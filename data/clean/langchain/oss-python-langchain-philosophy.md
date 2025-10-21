---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langchain-philosophy",
  "h1": "oss-python-langchain-philosophy",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.445557",
  "sha256_raw": "c000d551ddc80b4974eccfe173d3e0515b0cd0ab596a50a312eef7f5af2b59e4"
}
---

# oss-python-langchain-philosophy

> Source: https://docs.langchain.com/oss/python/langchain/philosophy

- LLMs are great, powerful new technology.
- LLMs are even better when you combine them with external sources of data.
- LLMs will transform what the applications of the future look like. Specifically, the applications of the future will look more and more agentic.
- It is still very early on in that transformation.
- While it’s easy to build a prototype of those agentic applications, it’s still really hard to build agents that are reliable enough to put into production.
We want to enable developers to build with the best models.
We want to make it easy to use models to orchestrate more complex flows that interact with other data and computation.
History
Given the constant rate of change in the field, LangChain has also evolved over time. Below is a brief timeline of how LangChain has changed over the years, evolving alongside what it means to build with LLMs:- LLM abstractions
- “Chains”, or predetermined steps of computation to run, for common use cases. For example - RAG: run a retrieval step, then run a generation step.
langchain-community
.langchain-core
message format accordingly to allow developers to specify these multimodal inputs in a standard way.-
Complete revamp of all chains and agents in
langchain
. All chains and agents are now replaced with only one high level abstraction: an agent abstraction built on top of LangGraph. This was the high-level abstraction that was originally created in LangGraph, but just moved to LangChain. For users still using old LangChain chains/agents who do NOT want to upgrade (note: we recommend you do), you can continue using old LangChain by installing thelangchain-classic
package. - A standard message content format: Model APIs evolved from returning messages with a simple content string to more complex output types - reasoning blocks, citations, server-side tool calls, etc. LangChain evolved its message formats to standardize these across providers.