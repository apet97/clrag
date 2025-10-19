# oss-python-integrations-providers-aws

> Source: https://docs.langchain.com/oss/python/integrations/providers/aws

Chat models
Bedrock Chat
Amazon Bedrock is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies likeSee a usage example.AI21 Labs
,Anthropic
,Cohere
,Meta
,Stability AI
, andAmazon
via a single API, along with a broad set of capabilities you need to build generative AI applications with security, privacy, and responsible AI. UsingAmazon Bedrock
, you can easily experiment with and evaluate top FMs for your use case, privately customize them with your data using techniques such as fine-tuning andRetrieval Augmented Generation
(RAG
), and build agents that execute tasks using your enterprise systems and data sources. SinceAmazon Bedrock
is serverless, you don’t have to manage any infrastructure, and you can securely integrate and deploy generative AI capabilities into your applications using the AWS services you are already familiar with.
Bedrock Converse
AWS Bedrock maintains a Converse API that provides a unified conversational interface for Bedrock models. This API does not yet support custom models. You can see a list of all models that are supported here.
See a usage example.
LLMs
Bedrock
See a usage example.Amazon API Gateway
Amazon API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale. APIs act as the “front door” for applications to access data, business logic, or functionality from your backend services. UsingSee a usage example.API Gateway
, you can create RESTful APIs and WebSocket APIs that enable real-time two-way communication applications.API Gateway
supports containerized and serverless workloads, as well as web applications.API Gateway
handles all the tasks involved in accepting and processing up to hundreds of thousands of concurrent API calls, including traffic management, CORS support, authorization and access control, throttling, monitoring, and API version management.API Gateway
has no minimum fees or startup costs. You pay for the API calls you receive and the amount of data transferred out and, with theAPI Gateway
tiered pricing model, you can reduce your cost as your API usage scales.
SageMaker Endpoint
Amazon SageMaker is a system that can build, train, and deploy machine learning (ML) models with fully managed infrastructure, tools, and workflows.We use
SageMaker
to host our model and expose it as the SageMaker Endpoint
.
See a usage example.
Embedding Models
Bedrock
See a usage example.SageMaker Endpoint
See a usage example.Document loaders
AWS S3 Directory and File
Amazon Simple Storage Service (Amazon S3) is an object storage service. AWS S3 Directory AWS S3 BucketsSee a usage example for S3DirectoryLoader. See a usage example for S3FileLoader.
Amazon Textract
Amazon Textract is a machine learning (ML) service that automatically extracts text, handwriting, and data from scanned documents.See a usage example.
Amazon Athena
Amazon Athena is a serverless, interactive analytics service built on open-source frameworks, supporting open-table and file formats.See a usage example.
AWS Glue
The AWS Glue Data Catalog is a centralized metadata repository that allows you to manage, access, and share metadata about your data stored in AWS. It acts as a metadata store for your data assets, enabling various AWS services and your applications to query and connect to the data they need efficiently.See a usage example.
Vector stores
Amazon OpenSearch Service
Amazon OpenSearch Service performs interactive log analytics, real-time application monitoring, website search, and more.We need to install several python libraries.OpenSearch
is an open source, distributed search and analytics suite derived fromElasticsearch
.Amazon OpenSearch Service
offers the latest versions ofOpenSearch
, support for many versions ofElasticsearch
, as well as visualization capabilities powered byOpenSearch Dashboards
andKibana
.
Amazon DocumentDB Vector Search
Amazon DocumentDB (with MongoDB Compatibility) makes it easy to set up, operate, and scale MongoDB-compatible databases in the cloud. With Amazon DocumentDB, you can run the same application code and use the same drivers and tools that you use with MongoDB. Vector search for Amazon DocumentDB combines the flexibility and rich querying capability of a JSON-based document database with the power of vector search.
Installation and Setup
See detail configuration instructions. We need to install thepymongo
python package.
Deploy DocumentDB on AWS
Amazon DocumentDB (with MongoDB Compatibility) is a fast, reliable, and fully managed database service. Amazon DocumentDB makes it easy to set up, operate, and scale MongoDB-compatible databases in the cloud. AWS offers services for computing, databases, storage, analytics, and other functionality. For an overview of all AWS services, see Cloud Computing with Amazon Web Services. See a usage example.Amazon MemoryDB
Amazon MemoryDB is a durable, in-memory database service that delivers ultra-fast performance. MemoryDB is compatible with Redis OSS, a popular open source data store, enabling you to quickly build applications using the same flexible and friendly Redis OSS APIs, and commands that they already use today. InMemoryVectorStore class provides a vectorstore to connect with Amazon MemoryDB.Retrievers
Amazon Kendra
Amazon Kendra is an intelligent search service provided byAmazon Web Services
(AWS
). It utilizes advanced natural language processing (NLP) and machine learning algorithms to enable powerful search capabilities across various data sources within an organization.Kendra
is designed to help users find the information they need quickly and accurately, improving productivity and decision-making.
With Kendra
, we can search across a wide range of content types, including documents, FAQs, knowledge bases,
manuals, and websites. It supports multiple languages and can understand complex queries, synonyms, and
contextual meanings to provide highly relevant search results.
We need to install the langchain-aws
library.
Amazon Bedrock (Knowledge Bases)
Knowledge bases for Amazon Bedrock is anWe need to install theAmazon Web Services
(AWS
) offering which lets you quickly build RAG applications by using your private data to customize foundation model response.
langchain-aws
library.
Tools
AWS Lambda
We need to installAmazon AWS Lambda
is a serverless computing service provided byAmazon Web Services
(AWS
). It helps developers to build and run applications and services without provisioning or managing servers. This serverless architecture enables you to focus on writing and deploying code, while AWS automatically takes care of scaling, patching, and managing the infrastructure required to run your applications.
boto3
python library.
Graphs
Amazon Neptune
Amazon Neptune is a high-performance graph analytics and serverless database for superior scalability and availability.For the Cypher and SPARQL integrations below, we need to install the
langchain-aws
library.
Amazon Neptune with Cypher
See a usage example.Amazon Neptune with SPARQL
Callbacks
Bedrock token usage
SageMaker Tracking
Amazon SageMaker is a fully managed service that is used to quickly and easily build, train and deploy machine learning (ML) models.
Amazon SageMaker Experiments is a capability
of Amazon SageMaker
that lets you organize, track,
compare and evaluate ML experiments and model versions.
We need to install several python libraries.
Chains
Amazon Comprehend Moderation Chain
Amazon Comprehend is a natural-language processing (NLP) service that uses machine learning to uncover valuable insights and connections in text.We need to install the
boto3
and nltk
libraries.