# oss-javascript-integrations-providers-microsoft

> Source: https://docs.langchain.com/oss/javascript/integrations/providers/microsoft

Microsoft Azure
and other Microsoft
products.
Chat Models
Azure OpenAI
See a usage exampleLLM
Azure OpenAI
Microsoft Azure, often referred to asAzure
is a cloud computing platform run byMicrosoft
, which offers access, management, and development of applications and services through global data centers. It provides a range of capabilities, including software as a service (SaaS), platform as a service (PaaS), and infrastructure as a service (IaaS).Microsoft Azure
supports many programming languages, tools, and frameworks, including Microsoft-specific and third-party software and systems.
Azure OpenAI is a cloud service to help you quickly develop generative AI experiences with a diverse set of prebuilt and curated models from OpenAI, Meta and beyond.LangChain.js supports integration with Azure OpenAI using the new Azure integration in the OpenAI SDK. You can learn more about Azure OpenAI and its difference with the OpenAI API on this page. If you don’t have an Azure account, you can create a free account to get started. You’ll need to have an Azure OpenAI instance deployed. You can deploy a version on Azure Portal following this guide. Once you have your instance running, make sure you have the name of your instance and key. You can find the key in the Azure Portal, under the “Keys and Endpoint” section of your instance. If you’re using Node.js, you can define the following environment variables to use the service:
npm
Text Embedding Models
Azure OpenAI
See a usage exampleVector stores
Azure AI Search
Azure AI Search (formerly known as Azure Search and Azure Cognitive Search) is a distributed, RESTful search engine optimized for speed and relevance on production-scale workloads on Azure. It supports also vector search using the k-nearest neighbor (kNN) algorithm and also semantic search.
npm
Azure Cosmos DB for NoSQL
Azure Cosmos DB for NoSQL provides support for querying items with flexible schemas and native support for JSON. It now offers vector indexing and search. This feature is designed to handle high-dimensional vectors, enabling efficient and accurate vector search at any scale. You can now store vectors directly in the documents alongside your data. Each document in your database can contain not only traditional schema-free data, but also high-dimensional vectors as other properties of the documents.
npm
Azure Cosmos DB for MongoDB vCore
Azure Cosmos DB for MongoDB vCore makes it easy to create a database with full native MongoDB support. You can apply your MongoDB experience and continue to use your favorite MongoDB drivers, SDKs, and tools by pointing your application to the API for MongoDB vCore account’s connection string. Use vector search in Azure Cosmos DB for MongoDB vCore to seamlessly integrate your AI-based applications with your data that’s stored in Azure Cosmos DB.
npm
Semantic Cache
Azure Cosmos DB NoSQL Semantic Cache
The Semantic Cache feature is supported with Azure Cosmos DB for NoSQL integration, enabling users to retrieve cached responses based on semantic similarity between the user input and previously cached results. It leverages AzureCosmosDBNoSQLVectorStore, which stores vector embeddings of cached prompts. These embeddings enable similarity-based searches, allowing the system to retrieve relevant cached results.
npm
Document loaders
Azure Blob Storage
Azure Blob Storage is Microsoft’s object storage solution for the cloud. Blob Storage is optimized for storing massive amounts of unstructured data. Unstructured data is data that doesn’t adhere to a particular data model or definition, such as text or binary data.
Azure Files offers fully managed file shares in the cloud that are accessible via the industry standard Server Message Block (SMB
) protocol, Network File System (NFS
) protocol, andAzure Files REST API
.Azure Files
are based on theAzure Blob Storage
.
Azure Blob Storage
is designed for:
- Serving images or documents directly to a browser.
- Storing files for distributed access.
- Streaming video and audio.
- Writing to log files.
- Storing data for backup and restore, disaster recovery, and archiving.
- Storing data for analysis by an on-premises or Azure-hosted service.
npm
Tools
Azure Container Apps Dynamic Sessions
Azure Container Apps dynamic sessions provide fast access to secure sandboxed environments that are ideal for running code or applications that require strong isolation from other workloads.
npm