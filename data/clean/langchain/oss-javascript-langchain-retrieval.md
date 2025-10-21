---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langchain-retrieval",
  "h1": "oss-javascript-langchain-retrieval",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.450038",
  "sha256_raw": "050efa188c52bba9e83d83f846966e6cbf4dfbb49d039718e82ecc7776d39543"
}
---

# oss-javascript-langchain-retrieval

> Source: https://docs.langchain.com/oss/javascript/langchain/retrieval

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
- Finite context — they can’t ingest entire corpora at once.
- Static knowledge — their training data is frozen at a point in time.
Building a knowledge base
A knowledge base is a repository of documents or structured data used during retrieval. If you need a custom knowledge base, you can use LangChain’s document loaders and vector stores to build one from your own data.If you already have a knowledge base (e.g., a SQL database, CRM, or internal documentation system), you do not need to rebuild it. You can:
- Connect it as a tool for an agent in Agentic RAG.
- Query it and supply the retrieved content as context to the LLM (2-Step RAG).
Tutorial: Semantic search
Learn how to create a searchable knowledge base from your own data using LangChain’s document loaders, embeddings, and vector stores.
In this tutorial, you’ll build a search engine over a PDF, enabling retrieval of passages relevant to a query. You’ll also implement a minimal RAG workflow on top of this engine to see how external knowledge can be integrated into LLM reasoning.
From retrieval to RAG
Retrieval allows LLMs to access relevant context at runtime. But most real-world applications go one step further: they integrate retrieval with generation to produce grounded, context-aware answers. This is the core idea behind Retrieval-Augmented Generation (RAG). The retrieval pipeline becomes a foundation for a broader system that combines search with generation.Retrieval Pipeline
A typical retrieval workflow looks like this: Each component is modular: you can swap loaders, splitters, embeddings, or vector stores without rewriting the app’s logic.Building Blocks
Embedding models
An embedding model turns text into a vector of numbers so that texts with similar meaning land close together in that vector space.
Vector stores
Specialized databases for storing and searching embeddings.
Retrievers
A retriever is an interface that returns documents given an unstructured query.
RAG Architectures
RAG can be implemented in multiple ways, depending on your system’s needs. We outline each type in the sections below.| Architecture | Description | Control | Flexibility | Latency | Example Use Case |
|---|---|---|---|---|---|
| 2-Step RAG | Retrieval always happens before generation. Simple and predictable | ✅ High | ❌ Low | ⚡ Fast | FAQs, documentation bots |
| Agentic RAG | An LLM-powered agent decides when and how to retrieve during reasoning | ❌ Low | ✅ High | ⏳ Variable | Research assistants with access to multiple tools |
| Hybrid | Combines characteristics of both approaches with validation steps | ⚖️ Medium | ⚖️ Medium | ⏳ Variable | Domain-specific Q&A with quality validation |
Latency: Latency is generally more predictable in 2-Step RAG, as the maximum number of LLM calls is known and capped. This predictability assumes that LLM inference time is the dominant factor. However, real-world latency may also be affected by the performance of retrieval steps—such as API response times, network delays, or database queries—which can vary based on the tools and infrastructure in use.
2-step RAG
In 2-Step RAG, the retrieval step is always executed before the generation step. This architecture is straightforward and predictable, making it suitable for many applications where the retrieval of relevant documents is a clear prerequisite for generating an answer.Tutorial: Retrieval-Augmented Generation (RAG)
See how to build a Q&A chatbot that can answer questions grounded in your data using Retrieval-Augmented Generation.
This tutorial walks through two approaches:
- A RAG agent that runs searches with a flexible tool—great for general-purpose use.
- A 2-step RAG chain that requires just one LLM call per query—fast and efficient for simpler tasks.
Agentic RAG
Agentic Retrieval-Augmented Generation (RAG) combines the strengths of Retrieval-Augmented Generation with agent-based reasoning. Instead of retrieving documents before answering, an agent (powered by an LLM) reasons step-by-step and decides when and how to retrieve information during the interaction.The only thing an agent needs to enable RAG behavior is access to one or more tools that can fetch external knowledge — such as documentation loaders, web APIs, or database queries.
Tutorial: Retrieval-Augmented Generation (RAG)
See how to build a Q&A chatbot that can answer questions grounded in your data using Retrieval-Augmented Generation.
This tutorial walks through two approaches:
- A RAG agent that runs searches with a flexible tool—great for general-purpose use.
- A 2-step RAG chain that requires just one LLM call per query—fast and efficient for simpler tasks.
Hybrid RAG
Hybrid RAG combines characteristics of both 2-Step and Agentic RAG. It introduces intermediate steps such as query preprocessing, retrieval validation, and post-generation checks. These systems offer more flexibility than fixed pipelines while maintaining some control over execution. Typical components include:- Query enhancement: Modify the input question to improve retrieval quality. This can involve rewriting unclear queries, generating multiple variations, or expanding queries with additional context.
- Retrieval validation: Evaluate whether retrieved documents are relevant and sufficient. If not, the system may refine the query and retrieve again.
- Answer validation: Check the generated answer for accuracy, completeness, and alignment with source content. If needed, the system can regenerate or revise the answer.
- Applications with ambiguous or underspecified queries
- Systems that require validation or quality control steps
- Workflows involving multiple sources or iterative refinement
Tutorial: Agentic RAG with Self-Correction
An example of Hybrid RAG that combines agentic reasoning with retrieval and self-correction.