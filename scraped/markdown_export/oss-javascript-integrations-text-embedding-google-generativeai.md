# oss-javascript-integrations-text-embedding-google-generativeai

> Source: https://docs.langchain.com/oss/javascript/integrations/text_embedding/google_generativeai

GoogleGenerativeAIEmbeddings
features and configuration options, please refer to the API reference.
Overview
Integration details
| Class | Package | Local | Py support | Downloads | Version |
|---|---|---|---|---|---|
GoogleGenerativeAIEmbeddings | @langchain/google-genai | ❌ | ✅ |
Setup
To access Google Generative AI embedding models you’ll need to sign up for a Google AI account, get an API key, and install the@langchain/google-genai
integration package.
Credentials
Get an API key here: ai.google.dev/tutorials/setup. Next, set your key as an environment variable namedGOOGLE_API_KEY
:
Installation
The LangChainGoogleGenerativeAIEmbeddings
integration lives in the @langchain/google-genai
package. You may also wish to install the official SDK:
Instantiation
Now we can instantiate our model object and embed text:Indexing and Retrieval
Embedding models are often used in retrieval-augmented generation (RAG) flows, both as part of indexing data as well as later retrieving it. For more detailed instructions, please see our RAG tutorials under the Learn tab. Below, see how to index and retrieve data using theembeddings
object we initialized above. In this example, we will index and retrieve a sample document using the demo MemoryVectorStore
.
Direct Usage
Under the hood, the vectorstore and retriever implementations are callingembeddings.embedDocument(...)
and embeddings.embedQuery(...)
to create embeddings for the text(s) used in fromDocuments
and the retriever’s invoke
operations, respectively.
You can directly call these methods to get embeddings for your own use cases.
Embed single texts
You can embed queries for search withembedQuery
. This generates a vector representation specific to the query:
Embed multiple texts
You can embed multiple texts for indexing withembedDocuments
. The internals used for this method may (but do not have to) differ from embedding queries:
API reference
For detailed documentation of allGoogleGenerativeAIEmbeddings
features and configurations head to the API reference.