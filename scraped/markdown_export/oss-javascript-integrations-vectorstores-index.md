# oss-javascript-integrations-vectorstores-index

> Source: https://docs.langchain.com/oss/javascript/integrations/vectorstores/index

Overview
A vector store stores embedded data and performs similarity search.Interface
LangChain provides a unified interface for vector stores, allowing you to:addDocuments
- Add documents to the store.delete
- Remove stored documents by ID.similaritySearch
- Query for semantically similar documents.
Initialization
Most vectorstores in LangChain accept an embedding model as an argument when initializing the vector store.Adding docuemnts
You can add documents to the vector store by using theaddDocuments
function.
Deleting documents
You can delete documents from the vector store by using thedelete
function.
Similarity search
Issue a semantic query usingsimilaritySearch
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
Memory
Memory
Chroma
Chroma
FAISS
FAISS
MongoDB
MongoDB
PGVector
PGVector
Pinecone
Pinecone
Qdrant
Qdrant