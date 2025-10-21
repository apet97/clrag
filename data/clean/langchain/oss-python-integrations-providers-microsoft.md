---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-integrations-providers-microsoft",
  "h1": "oss-python-integrations-providers-microsoft",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.462238",
  "sha256_raw": "05c422d5cef4aa12486c0b29aa71217184facc8eebe021923096ae5354b5ef0c"
}
---

# oss-python-integrations-providers-microsoft

> Source: https://docs.langchain.com/oss/python/integrations/providers/microsoft

Microsoft Azure, often referred to as Azure is a cloud computing platform run by Microsoft, which offers access, management, and development of applications and services through global data centers. It provides a range of capabilities, including software as a service (SaaS), platform as a service (PaaS), and infrastructure as a service (IaaS). Microsoft Azure supports many programming languages, tools, and frameworks, including Microsoft-specific and third-party software and systems.
Azure OpenAI is an Azure service with powerful language models from OpenAI including the GPT-3, Codex and Embeddings model series for content generation, summarization, semantic search, and natural language to code translation.
Copy
pip install langchain-openai
Set the environment variables to get access to the Azure OpenAI service.
Azure AI Foundry provides access to a wide range of models from various providers including Azure OpenAI, DeepSeek R1, Cohere, Phi and Mistral through the AzureAIChatCompletionsModel class.
Azure AI Document Intelligence (formerly known
as Azure Form Recognizer) is machine-learning
based service that extracts texts (including handwriting), tables, document structures,
and key-value-pairs
from digital or scanned PDFs, images, Office and HTML files.Document Intelligence supports PDF, JPEG/JPG, PNG, BMP, TIFF, HEIF, DOCX, XLSX, PPTX and HTML.
Azure Blob Storage is Microsoft’s object storage solution for the cloud. Blob Storage is optimized for storing massive amounts of unstructured data. Unstructured data is data that doesn’t adhere to a particular data model or definition, such as text or binary data.
Azure Files offers fully managed
file shares in the cloud that are accessible via the industry standard Server Message Block (SMB) protocol,
Network File System (NFS) protocol, and Azure Files REST API. Azure Files are based on the Azure Blob Storage.
Azure Blob Storage is designed for:
Serving images or documents directly to a browser.
Storing files for distributed access.
Streaming video and audio.
Writing to log files.
Storing data for backup and restore, disaster recovery, and archiving.
Storing data for analysis by an on-premises or Azure-hosted service.
Microsoft Excel is a spreadsheet editor developed by
Microsoft for Windows, macOS, Android, iOS and iPadOS.
It features calculation or computation capabilities, graphing tools, pivot tables, and a macro programming
language called Visual Basic for Applications (VBA). Excel forms part of the Microsoft 365 suite of software.
The UnstructuredExcelLoader is used to load Microsoft Excel files. The loader works with both .xlsx and .xls files.
The page content will be the raw text of the Excel file. If you use the loader in "elements" mode, an HTML
representation of the Excel file will be available in the document metadata under the text_as_html key.See a usage example.
Copy
from langchain_community.document_loaders import UnstructuredExcelLoader
Microsoft SharePoint is a website-based collaboration system
that uses workflow applications, “list” databases, and other web parts and security features to
empower business teams to work together developed by Microsoft.
Playwright is an open-source automation tool
developed by Microsoft that allows you to programmatically control and automate
web browsers. It is designed for end-to-end testing, scraping, and automating
tasks across various web browsers such as Chromium, Firefox, and WebKit.
AI agents can rely on Azure Cosmos DB as a unified memory system solution, enjoying speed, scale, and simplicity. This service successfully enabled OpenAI’s ChatGPT service to scale dynamically with high reliability and low maintenance. Powered by an atom-record-sequence engine, it is the world’s first globally distributed NoSQL, relational, and vector database service that offers a serverless mode.Below are two available Azure Cosmos DB APIs that can provide vector store functionalities.
Azure Cosmos DB for MongoDB vCore makes it easy to create a database with full native MongoDB support.
You can apply your MongoDB experience and continue to use your favorite MongoDB drivers, SDKs, and tools by pointing your application to the API for MongoDB vCore account’s connection string.
Use vector search in Azure Cosmos DB for MongoDB vCore to seamlessly integrate your AI-based applications with your data that’s stored in Azure Cosmos DB.
Azure Cosmos DB for MongoDB vCore provides developers with a fully managed MongoDB-compatible database service for building modern applications with a familiar architecture.With Cosmos DB for MongoDB vCore, developers can enjoy the benefits of native Azure integrations, low total cost of ownership (TCO), and the familiar vCore architecture when migrating existing applications or building new ones.Sign Up for free to get started today.See a usage example.
Copy
from langchain_community.vectorstores import AzureCosmosDBVectorSearch
Azure Cosmos DB for NoSQL now offers vector indexing and search in preview.
This feature is designed to handle high-dimensional vectors, enabling efficient and accurate vector search at any scale. You can now store vectors
directly in the documents alongside your data. This means that each document in your database can contain not only traditional schema-free data,
but also high-dimensional vectors as other properties of the documents. This colocation of data and vectors allows for efficient indexing and searching,
as the vectors are stored in the same logical unit as the data they represent. This simplifies data management, AI application architectures, and the
efficiency of vector-based operations.
Azure Cosmos DB offers a solution for modern apps and intelligent workloads by being very responsive with dynamic and elastic autoscale. It is available
in every Azure region and can automatically replicate data closer to users. It has SLA guaranteed low-latency and high availability.Sign Up for free to get started today.See a usage example.
Copy
from langchain_community.vectorstores import AzureCosmosDBNoSQLVectorSearch
Azure Database for PostgreSQL - Flexible Server is a relational database service based on the open-source Postgres database engine. It’s a fully managed database-as-a-service that can handle mission-critical workloads with predictable performance, security, high availability, and dynamic scalability.
See set up instructions for Azure Database for PostgreSQL.Simply use the connection string from your Azure Portal.Since Azure Database for PostgreSQL is open-source Postgres, you can use the LangChain’s Postgres support to connect to Azure Database for PostgreSQL.
Azure SQL Database is a robust service that combines scalability, security, and high availability, providing all the benefits of a modern database solution. It also provides a dedicated Vector data type & built-in functions that simplifies the storage and querying of vector embeddings directly within a relational database. This eliminates the need for separate vector databases and related integrations, increasing the security of your solutions while reducing the overall complexity.
By leveraging your current SQL Server databases for vector search, you can enhance data capabilities while minimizing expenses and avoiding the challenges of transitioning to new systems.
Azure AI Search is a cloud search service
that gives developers infrastructure, APIs, and tools for information retrieval of vector, keyword, and hybrid
queries at scale. See here for usage examples.
Copy
from langchain_community.vectorstores.azuresearch import AzureSearch
Azure AI Search (formerly known as Azure Search or Azure Cognitive Search ) is a cloud search service that gives developers infrastructure, APIs, and tools for building a rich search experience over private, heterogeneous content in web, mobile, and enterprise applications.
Search is foundational to any app that surfaces text to users, where common scenarios include catalog or document search, online retail apps, or data exploration over proprietary content. When you create a search service, you’ll work with the following capabilities:
A search engine for full text search over a search index containing user-owned content
Rich indexing, with lexical analysis and optional AI enrichment for content extraction and transformation
Rich query syntax for text search, fuzzy search, autocomplete, geo-search and more
Programmability through REST APIs and client libraries in Azure SDKs
Azure integration at the data layer, machine learning layer, and AI (AI Services)
Azure Database for PostgreSQL - Flexible Server is a relational database service based on the open-source Postgres database engine. It’s a fully managed database-as-a-service that can handle mission-critical workloads with predictable performance, security, high availability, and dynamic scalability.
We need to get the POOL_MANAGEMENT_ENDPOINT environment variable from the Azure Container Apps service.
See the instructions here.We need to install a python package.
Follow the documentation here to get a detail explanations and instructions of this tool.The environment variable BING_SUBSCRIPTION_KEY and BING_SEARCH_URL are required from Bing Search resource.
Playwright is an open-source automation tool
developed by Microsoft that allows you to programmatically control and automate
web browsers. It is designed for end-to-end testing, scraping, and automating
tasks across various web browsers such as Chromium, Firefox, and WebKit.
Presidio (Origin from Latin praesidium ‘protection, garrison’)
helps to ensure sensitive data is properly managed and governed. It provides fast identification and
anonymization modules for private entities in text and images such as credit card numbers, names,
locations, social security numbers, bitcoin wallets, US phone numbers, financial data and more.
First, you need to install several python packages and download a SpaCy model.