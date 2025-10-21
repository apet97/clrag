---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-contributing-implement-langchain",
  "h1": "oss-python-contributing-implement-langchain",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.470952",
  "sha256_raw": "b653573aba6e4f0a7ca1340e497ce05a7e72b2770c8e8a0bc64216aea2b44a63"
}
---

# oss-python-contributing-implement-langchain

> Source: https://docs.langchain.com/oss/python/contributing/implement-langchain

Integration packages are Python packages that users can install for use in their projects. They implement one or more components that adhere to the LangChain interface standards.LangChain components are subclasses of base classes in langchain-core. Examples include chat models, tools, retrievers, and more.Your integration package will typically implement a subclass of at least one of these components. Expand the tabs below to see details on each.
Chat Models
Tools
Retrievers
Vector Stores
Embeddings
Chat models are subclasses of the BaseChatModel class. They implement methods for generating chat completions, handling message formatting, and managing model parameters.
The chat model integration guide is currently WIP. In the meantime, read the chat model conceptual guide for details on how LangChain chat models function.