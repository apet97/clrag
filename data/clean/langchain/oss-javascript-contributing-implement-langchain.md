---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-contributing-implement-langchain",
  "h1": "oss-javascript-contributing-implement-langchain",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.466554",
  "sha256_raw": "c00cf09877bd02f2da649ef5f19e9428f10b2fdab568ec9940699f964ff693f6"
}
---

# oss-javascript-contributing-implement-langchain

> Source: https://docs.langchain.com/oss/javascript/contributing/implement-langchain

langchain-core
. Examples include chat models, tools, retrievers, and more.
Your integration package will typically implement a subclass of at least one of these components. Expand the tabs below to see details on each.
- Chat Models
- Tools
- Retrievers
- Vector Stores
- Embeddings
Chat models are subclasses of the @[
BaseChatModel
] class. They implement methods for generating chat completions, handling message formatting, and managing model parameters.