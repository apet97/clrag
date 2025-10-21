---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-contributing-integrations-langchain",
  "h1": "oss-python-contributing-integrations-langchain",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.448559",
  "sha256_raw": "54a36ac3d5022846552db91bb05de6f883a625c9d69d56a9831256ba166ac859"
}
---

# oss-python-contributing-integrations-langchain

> Source: https://docs.langchain.com/oss/python/contributing/integrations-langchain

Why contribute an integration to LangChain?
Discoverability
LangChain is the most used framework for building LLM applications, with over 20 million monthly downloads.
Interoperability
LangChain components expose a standard interface, allowing developers to easily swap them for each other. If you implement a LangChain integration, any developer using a different component will easily be able to swap yours in.
Best Practices
Through their standard interface, LangChain components encourage and facilitate best practices (streaming, async, etc.) that improve developer experience and application performance.
Components to integrate
While any component can be integrated into LangChain, there are specific types of integrations we encourage more: Integrate these ✅:- Chat Models: Most actively used component type
- Tools/Toolkits: Enable agent capabilities
- Retrievers: Core to RAG applications
- Embedding Models: Foundation for vector operations
- Vector Stores: Essential for semantic search
- LLMs (Text-Completion Models): Deprecated in favor of Chat Models
- Document Loaders: High maintenance burden
- Key-Value Stores: Limited usage
- Document Transformers: Niche use cases
- Model Caches: Infrastructure concerns
- Graphs: Complex abstractions
- Message Histories: Storage abstractions
- Callbacks: System-level components
- Chat Loaders: Limited demand
- Adapters: Edge case utilities
How to contribute an integration
1
3
5
Add documentation
Open a PR to add documentation for your integration to the official LangChain docs.
Integration documentation guide
Integration documentation guide
An integration is only as useful as its documentation. To ensure a consistent experience for users, docs are required for all new integrations. We have a standard starting-point template for each type of integration for you to copy and modify.In a new PR to the LangChain docs repo, create a new file in the relevant directory under
src/oss/python/integrations/<component_type>/integration_name.mdx
using the appropriate template file:- Chat models
- Tools and toolkits
- Retrievers
- Text splitters - Coming soon
- Embedding models - Coming soon
- Vector stores
- Document loaders - Coming soon
- Key-value stores - Coming soon