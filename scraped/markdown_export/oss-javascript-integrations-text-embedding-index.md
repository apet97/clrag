# oss-javascript-integrations-text-embedding-index

> Source: https://docs.langchain.com/oss/javascript/integrations/text_embedding/index

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
LangChain provides a standard interface for text embedding models (e.g., OpenAI, Cohere, Hugging Face) via the Embeddings interface. Two main methods are available:embedDocuments(documents: string[]) → number[][]
: Embeds a list of documents.embedQuery(text: string) → number[]
: Embeds a single query.
The interface allows queries and documents to be embedded with different strategies, though most providers handle them the same way in practice.
Install and use
OpenAI
OpenAI
Install dependencies:Add environment variables:Instantiate the model:
Azure
Azure
Install dependenciesAdd environment variables:Instantiate the model:
AWS
AWS
Install dependencies:Add environment variables:Instantiate the model:
Google Gemini
Google Gemini
Install dependencies:Add environment variables:Instantiate the model:
Google Vertex
Google Vertex
Install dependencies:Add environment variables:Instantiate the model:
MistralAI
MistralAI
Install dependencies:Add environment variables:Instantiate the model:
Cohere
Cohere
Install dependencies:Add environment variables:Instantiate the model:
Ollama
Ollama
Install dependencies:Instantiate the model:
Caching
Embeddings can be stored or temporarily cached to avoid needing to recompute them. Caching embeddings can be done using aCacheBackedEmbeddings
. This wrapper stores embeddings in a key-value store, where the text is hashed and the hash is used as the key in the cache.
The main supported way to initialize a CacheBackedEmbeddings
is fromBytesStore
. It takes the following parameters:
- underlyingEmbeddings: The embedder to use for embedding.
- documentEmbeddingStore: Any
BaseStore
for caching document embeddings. - options.namespace: (optional, defaults to
""
) The namespace to use for the document cache. Helps avoid collisions (e.g., set it to the embedding model name).