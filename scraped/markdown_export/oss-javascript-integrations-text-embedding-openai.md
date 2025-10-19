# oss-javascript-integrations-text-embedding-openai

> Source: https://docs.langchain.com/oss/javascript/integrations/text_embedding/openai

This will help you get started with OpenAIEmbeddings embedding models using LangChain. For detailed documentation on OpenAIEmbeddings features and configuration options, please refer to the API reference.
To access OpenAIEmbeddings embedding models you’ll need to create an OpenAI account, get an API key, and install the @langchain/openai integration package.
Now we can instantiate our model object and generate chat completions:
Copy
import { OpenAIEmbeddings } from "@langchain/openai";const embeddings = new OpenAIEmbeddings({ apiKey: "YOUR-API-KEY", // In Node.js defaults to process.env.OPENAI_API_KEY batchSize: 512, // Default value if omitted is 512. Max is 2048 model: "text-embedding-3-large",});
If you’re part of an organization, you can set process.env.OPENAI_ORGANIZATION to your OpenAI organization id, or pass it in as organization when
initializing the model.
Embedding models are often used in retrieval-augmented generation (RAG) flows, both as part of indexing data as well as later retrieving it. For more detailed instructions, please see our RAG tutorials under the Learn tab.Below, see how to index and retrieve data using the embeddings object we initialized above. In this example, we will index and retrieve a sample document using the demo MemoryVectorStore.
Copy
// Create a vector store with a sample textimport { MemoryVectorStore } from "@langchain/classic/vectorstores/memory";const text = "LangChain is the framework for building context-aware reasoning applications";const vectorstore = await MemoryVectorStore.fromDocuments( [{ pageContent: text, metadata: {} }], embeddings,);// Use the vector store as a retriever that returns a single documentconst retriever = vectorstore.asRetriever(1);// Retrieve the most similar textconst retrievedDocuments = await retriever.invoke("What is LangChain?");retrievedDocuments[0].pageContent;
Copy
LangChain is the framework for building context-aware reasoning applications
Under the hood, the vectorstore and retriever implementations are calling embeddings.embedDocument(...) and embeddings.embedQuery(...) to create embeddings for the text(s) used in fromDocuments and the retriever’s invoke operations, respectively.You can directly call these methods to get embeddings for your own use cases.
You can embed multiple texts for indexing with embedDocuments. The internals used for this method may (but do not have to) differ from embedding queries:
Copy
const text2 = "LangGraph is a library for building stateful, multi-actor applications with LLMs";const vectors = await embeddings.embedDocuments([text, text2]);console.log(vectors[0].slice(0, 100));console.log(vectors[1].slice(0, 100));
With the text-embedding-3 class of models, you can specify the size of the embeddings you want returned. For example by default text-embedding-3-large returns embeddings of dimension 3072:
Copy
import { OpenAIEmbeddings } from "@langchain/openai";const embeddingsDefaultDimensions = new OpenAIEmbeddings({ model: "text-embedding-3-large",});const vectorsDefaultDimensions = await embeddingsDefaultDimensions.embedDocuments(["some text"]);console.log(vectorsDefaultDimensions[0].length);
Copy
3072
But by passing in dimensions: 1024 we can reduce the size of our embeddings to 1024:
Copy
import { OpenAIEmbeddings } from "@langchain/openai";const embeddings1024 = new OpenAIEmbeddings({ model: "text-embedding-3-large", dimensions: 1024,});const vectors1024 = await embeddings1024.embedDocuments(["some text"]);console.log(vectors1024[0].length);
You can customize the base URL the SDK sends requests to by passing a configuration parameter like this:
Copy
import { OpenAIEmbeddings } from "@langchain/openai";const model = new OpenAIEmbeddings({ configuration: { baseURL: "https://your_custom_url.com", },});
You can also pass other ClientOptions parameters accepted by the official SDK.If you are hosting on Azure OpenAI, see the dedicated page instead.