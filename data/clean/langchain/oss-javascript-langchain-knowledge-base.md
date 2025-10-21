---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langchain-knowledge-base",
  "h1": "oss-javascript-langchain-knowledge-base",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.436162",
  "sha256_raw": "398127ad01c7f9783cef8c814489258524946525b5418e9662108af2b5adc8b4"
}
---

# oss-javascript-langchain-knowledge-base

> Source: https://docs.langchain.com/oss/javascript/langchain/knowledge-base

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Overview
This tutorial will familiarize you with LangChain’s document loader, embedding, and vector store abstractions. These abstractions are designed to support retrieval of data— from (vector) databases and other sources — for integration with LLM workflows. They are important for applications that fetch data to be reasoned over as part of model inference, as in the case of retrieval-augmented generation, or RAG. Here we will build a search engine over a PDF document. This will allow us to retrieve passages in the PDF that are similar to an input query. The guide also includes a minimal RAG implementation on top of the search engine.Concepts
This guide focuses on retrieval of text data. We will cover the following concepts:Setup
Installation
This guide requires@langchain/community
and pdf-parse
:
LangSmith
Many of the applications you build with LangChain will contain multiple steps with multiple invocations of LLM calls. As these applications get more and more complex, it becomes crucial to be able to inspect what exactly is going on inside your chain or agent. The best way to do this is with LangSmith. After you sign up at the link above, make sure to set your environment variables to start logging traces:1. Documents and Document Loaders
LangChain implements a Document abstraction, which is intended to represent a unit of text and associated metadata. It has three attributes:pageContent
: a string representing the content;metadata
: a dict containing arbitrary metadata;id
: (optional) a string identifier for the document.
metadata
attribute can capture information about the source of the document, its relationship to other documents, and other information. Note that an individual Document
object often represents a chunk of a larger document.
We can generate sample documents when desired:
Loading documents
Let’s load a PDF into a sequence ofDocument
objects. Here is a sample PDF — a 10-k filing for Nike from 2023. We can consult the LangChain documentation for available PDF document loaders.
PDFLoader
loads one Document
object per PDF page. For each, we can easily access:
- The string content of the page;
- Metadata containing the file name and page number.
Splitting
For both information retrieval and downstream question-answering purposes, a page may be too coarse a representation. Our goal in the end will be to retrieveDocument
objects that answer an input query, and further splitting our PDF will help ensure that the meanings of relevant portions of the document are not “washed out” by surrounding text.
We can use text splitters for this purpose. Here we will use a simple text splitter that partitions based on characters. We will split our documents into chunks of 1000 characters
with 200 characters of overlap between chunks. The overlap helps
mitigate the possibility of separating a statement from important
context related to it. We use the
RecursiveCharacterTextSplitter
,
which will recursively split the document using common separators like
new lines until each chunk is the appropriate size. This is the
recommended text splitter for generic text use cases.
2. Embeddings
Vector search is a common way to store and search over unstructured data (such as unstructured text). The idea is to store numeric vectors that are associated with the text. Given a query, we can embed it as a vector of the same dimension and use vector similarity metrics (such as cosine similarity) to identify related text. LangChain supports embeddings from dozens of providers. These models specify how text should be converted into a numeric vector. Let’s select a model:- OpenAI
- Azure
- AWS
- VertexAI
- MistralAI
- Cohere
3. Vector stores
LangChain @[VectorStore] objects contain methods for adding text andDocument
objects to the store, and querying them using various similarity metrics. They are often initialized with embedding models, which determine how text data is translated to numeric vectors.
LangChain includes a suite of integrations with different vector store technologies. Some vector stores are hosted by a provider (e.g., various cloud providers) and require specific credentials to use; some (such as Postgres) run in separate infrastructure that can be run locally or via a third-party; others can run in-memory for lightweight workloads. Let’s select a vector store:
- Memory
- Chroma
- FAISS
- MongoDB
- PGVector
- Pinecone
- Qdrant
VectorStore
] that contains documents, we can query it. @[VectorStore] includes methods for querying:
- Synchronously and asynchronously;
- By string query and by vector;
- With and without returning similarity scores;
- By similarity and @[maximum marginal relevance][VectorStore.max_marginal_relevance_search] (to balance similarity with query to diversity in retrieved results).
- @[API Reference][VectorStore]
- Integration-specific docs
4. Retrievers
LangChain @[VectorStore
] objects do not subclass @[Runnable]. LangChain @[Retrievers] are Runnables, so they implement a standard set of methods (e.g., synchronous and asynchronous invoke
and batch
operations). Although we can construct retrievers from vector stores, retrievers can interface with non-vector store sources of data, as well (such as external APIs).
Vectorstores implement an as_retriever
method that will generate a Retriever, specifically a VectorStoreRetriever. These retrievers include specific search_type
and search_kwargs
attributes that identify what methods of the underlying vector store to call, and how to parameterize them. For instance, we can replicate the above with the following: