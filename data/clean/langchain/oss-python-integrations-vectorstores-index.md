---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-integrations-vectorstores-index",
  "h1": "oss-python-integrations-vectorstores-index",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.472335",
  "sha256_raw": "afde664a272ada616cff70c9d5dcd4c548a5e618c9af24188f99cb26550fe2c9"
}
---

# oss-python-integrations-vectorstores-index

> Source: https://docs.langchain.com/oss/python/integrations/vectorstores/index

Overview
A vector store stores embedded data and performs similarity search.Interface
LangChain provides a unified interface for vector stores, allowing you to:add_documents
- Add documents to the store.delete
- Remove stored documents by ID.similarity_search
- Query for semantically similar documents.
Initialization
To initialize a vector store, provide it with an embedding model:Adding documents
AddDocument
objects (holding page_content
and optional metadata) like so:
Deleting documents
Delete by specifying IDs:Similarity search
Issue a semantic query usingsimilarity_search
, which returns the closest embedded documents:
k
— number of results to returnfilter
— conditional filtering based on metadata
Similarity metrics & indexing
Embedding similarity may be computed using:- Cosine similarity
- Euclidean distance
- Dot product
Metadata filtering
Filtering by metadata (e.g., source, date) can refine search results:Top integrations
Select embedding model:OpenAI
OpenAI
Azure
Azure
Google Gemini
Google Gemini
Google Vertex
Google Vertex
AWS
AWS
HuggingFace
HuggingFace
Ollama
Ollama
Cohere
Cohere
Mistral AI
Mistral AI
Nomic
Nomic
NVIDIA
NVIDIA
Voyage AI
Voyage AI
IBM watsonx
IBM watsonx
Fake
Fake
xAI
xAI
Perplexity
Perplexity
DeepSeek
DeepSeek
In-memory
In-memory
AstraDB
AstraDB
Chroma
Chroma
FAISS
FAISS
Milvus
Milvus
MongoDB
MongoDB
PGVector
PGVector
PGVectorStore
PGVectorStore
Pinecone
Pinecone
Qdrant
Qdrant
| Vectorstore | Delete by ID | Filtering | Search by Vector | Search with score | Async | Passes Standard Tests | Multi Tenancy | IDs in add Documents |
|---|---|---|---|---|---|---|---|---|
AstraDBVectorStore | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
Chroma | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
Clickhouse | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
CouchbaseSearchVectorStore | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
DatabricksVectorSearch | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
ElasticsearchStore | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
FAISS | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
InMemoryVectorStore | ✅ | ✅ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ |
Milvus | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
Moorcheh | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
MongoDBAtlasVectorSearch | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
openGauss | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ |
PGVector | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
PGVectorStore | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
PineconeVectorStore | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ✅ |
QdrantVectorStore | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
Weaviate | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
SQLServer | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
ZeusDB | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |