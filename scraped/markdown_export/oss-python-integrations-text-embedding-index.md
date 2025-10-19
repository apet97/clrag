# oss-python-integrations-text-embedding-index

> Source: https://docs.langchain.com/oss/python/integrations/text_embedding/index

Overview
This overview covers text-based embedding models. LangChain does not currently support multimodal embeddings.
How it works
- Vectorization — The model encodes each input string as a high-dimensional vector.
- Similarity scoring — Vectors are compared using mathematical metrics to measure how closely related the underlying texts are.
Similarity metrics
Several metrics are commonly used to compare embeddings:- Cosine similarity — measures the angle between two vectors.
- Euclidean distance — measures the straight-line distance between points.
- Dot product — measures how much one vector projects onto another.
Interface
LangChain provides a standard interface for text embedding models (e.g., OpenAI, Cohere, Hugging Face) via the Embeddings interface. Two main methods are available:embed_documents(texts: List[str]) → List[List[float]]
: Embeds a list of documents.embed_query(text: str) → List[float]
: Embeds a single query.
The interface allows queries and documents to be embedded with different strategies, though most providers handle them the same way in practice.
Top integrations
Caching
Embeddings can be stored or temporarily cached to avoid needing to recompute them. Caching embeddings can be done using aCacheBackedEmbeddings
. This wrapper stores embeddings in a key-value store, where the text is hashed and the hash is used as the key in the cache.
The main supported way to initialize a CacheBackedEmbeddings
is from_bytes_store
. It takes the following parameters:
underlying_embedder
: The embedder to use for embedding.document_embedding_cache
: AnyByteStore
for caching document embeddings.batch_size
: (optional, defaults toNone
) The number of documents to embed between store updates.namespace
: (optional, defaults to""
) The namespace to use for the document cache. Helps avoid collisions (e.g., set it to the embedding model name).query_embedding_cache
: (optional, defaults toNone
) AByteStore
for caching query embeddings, orTrue
to reuse the same store asdocument_embedding_cache
.