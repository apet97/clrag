---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-integrations-text-embedding-azure-openai",
  "h1": "oss-javascript-integrations-text-embedding-azure-openai",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.487790",
  "sha256_raw": "dcbdcb7bd57a9d22243c2196e4af1aa9409fc143533f2585b9aa74731bbbd776"
}
---

# oss-javascript-integrations-text-embedding-azure-openai

> Source: https://docs.langchain.com/oss/javascript/integrations/text_embedding/azure_openai

Azure OpenAI is a cloud service to help you quickly develop generative AI experiences with a diverse set of prebuilt and curated models from OpenAI, Meta and beyond.LangChain.js supports integration with Azure OpenAI using the new Azure integration in the OpenAI SDK.You can learn more about Azure OpenAI and its difference with the OpenAI API on this page. If you don’t have an Azure account, you can create a free account to get started.This will help you get started with AzureOpenAIEmbeddings embedding models using LangChain. For detailed documentation on AzureOpenAIEmbeddings features and configuration options, please refer to the API reference.
Copy
<Info>**Previously, LangChain.js supported integration with Azure OpenAI using the dedicated [Azure OpenAI SDK](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai). This SDK is now deprecated in favor of the new Azure integration in the OpenAI SDK, which allows to access the latest OpenAI models and features the same day they are released, and allows seamless transition between the OpenAI API and Azure OpenAI.**If you are using Azure OpenAI with the deprecated SDK, see the [migration guide](#migration-from-azure-openai-sdk) to update to the new API.</Info>
You’ll need to have an Azure OpenAI instance deployed. You can deploy a version on Azure Portal following this guide.Once you have your instance running, make sure you have the name of your instance and key. You can find the key in the Azure Portal, under the “Keys and Endpoint” section of your instance.If you’re using Node.js, you can define the following environment variables to use the service:
The LangChain AzureOpenAIEmbeddings integration lives in the @langchain/openai package:
Copy
import IntegrationInstallTooltip from "@mdx_components/integration_install_tooltip.mdx";<IntegrationInstallTooltip></IntegrationInstallTooltip><Npm2Yarn> @langchain/openai @langchain/core</Npm2Yarn><Info>**You can find the list of supported API versions in the [Azure OpenAI documentation](https://learn.microsoft.com/azure/ai-services/openai/reference).**</Info><Tip>**If `AZURE_OPENAI_API_EMBEDDINGS_DEPLOYMENT_NAME` is not defined, it will fall back to the value of `AZURE_OPENAI_API_DEPLOYMENT_NAME` for the deployment name. The same applies to the `azureOpenAIApiEmbeddingsDeploymentName` parameter in the `AzureOpenAIEmbeddings` constructor, which will fall back to the value of `azureOpenAIApiDeploymentName` if not defined.**</Tip>
Now we can instantiate our model object and embed text:
Copy
import { AzureOpenAIEmbeddings } from "@langchain/openai";const embeddings = new AzureOpenAIEmbeddings({ azureOpenAIApiKey: "<your_key>", // In Node.js defaults to process.env.AZURE_OPENAI_API_KEY azureOpenAIApiInstanceName: "<your_instance_name>", // In Node.js defaults to process.env.AZURE_OPENAI_API_INSTANCE_NAME azureOpenAIApiEmbeddingsDeploymentName: "<your_embeddings_deployment_name>", // In Node.js defaults to process.env.AZURE_OPENAI_API_EMBEDDINGS_DEPLOYMENT_NAME azureOpenAIApiVersion: "<api_version>", // In Node.js defaults to process.env.AZURE_OPENAI_API_VERSION maxRetries: 1,});
Embedding models are often used in retrieval-augmented generation (RAG) flows, both as part of indexing data as well as later retrieving it. For more detailed instructions, please see our RAG tutorials under the Learn tab.Below, see how to index and retrieve data using the embeddings object we initialized above. In this example, we will index and retrieve a sample document using the demo MemoryVectorStore.
Copy
// Create a vector store with a sample textimport { MemoryVectorStore } from "@langchain/classic/vectorstores/memory";const text = "LangChain is the framework for building context-aware reasoning applications";const vectorstore = await MemoryVectorStore.fromDocuments( [{ pageContent: text, metadata: {} }], embeddings,);// Use the vector store as a retriever that returns a single documentconst retriever = vectorstore.asRetriever(1);// Retrieve the most similar textconst retrievedDocuments = await retriever.invoke("What is LangChain?");retrievedDocuments[0].pageContent;
Copy
LangChain is the framework for building context-aware reasoning applications
Under the hood, the vectorstore and retriever implementations are calling embeddings.embedDocument(...) and embeddings.embedQuery(...) to create embeddings for the text(s) used in fromDocuments and the retriever’s invoke operations, respectively.You can directly call these methods to get embeddings for your own use cases.
You can embed multiple texts for indexing with embedDocuments. The internals used for this method may (but do not have to) differ from embedding queries:
Copy
const text2 = "LangGraph is a library for building stateful, multi-actor applications with LLMs";const vectors = await embeddings.embedDocuments([text, text2]);console.log(vectors[0].slice(0, 100));console.log(vectors[1].slice(0, 100));
If your instance is hosted under a domain other than the default openai.azure.com, you’ll need to use the alternate AZURE_OPENAI_BASE_PATH environment variable.
For example, here’s how you would connect to the domain https://westeurope.api.microsoft.com/openai/deployments/{DEPLOYMENT_NAME}:
Copy
import { AzureOpenAIEmbeddings } from "@langchain/openai";const embeddingsDifferentDomain = new AzureOpenAIEmbeddings({ azureOpenAIApiKey: "<your_key>", // In Node.js defaults to process.env.AZURE_OPENAI_API_KEY azureOpenAIApiEmbeddingsDeploymentName: "<your_embedding_deployment_name>", // In Node.js defaults to process.env.AZURE_OPENAI_API_EMBEDDINGS_DEPLOYMENT_NAME azureOpenAIApiVersion: "<api_version>", // In Node.js defaults to process.env.AZURE_OPENAI_API_VERSION azureOpenAIBasePath: "https://westeurope.api.microsoft.com/openai/deployments", // In Node.js defaults to process.env.AZURE_OPENAI_BASE_PATH});
The configuration field also accepts other ClientOptions parameters accepted by the official SDK.Note: The specific header api-key currently cannot be overridden in this manner and will pass through the value from azureOpenAIApiKey.
If you are using the deprecated Azure OpenAI SDK with the @langchain/azure-openai package, you can update your code to use the new Azure integration following these steps:
Install the new @langchain/openai package and remove the previous @langchain/azure-openai package:
Update your imports to use the new AzureOpenAIEmbeddings classe from the @langchain/openai package:
Copy
import { AzureOpenAIEmbeddings } from "@langchain/openai";
Update your code to use the new AzureOpenAIEmbeddings class and pass the required parameters:
Copy
const model = new AzureOpenAIEmbeddings({ azureOpenAIApiKey: "<your_key>", azureOpenAIApiInstanceName: "<your_instance_name>", azureOpenAIApiEmbeddingsDeploymentName: "<your_embeddings_deployment_name>", azureOpenAIApiVersion: "<api_version>",});
Notice that the constructor now requires the azureOpenAIApiInstanceName parameter instead of the azureOpenAIEndpoint parameter, and adds the azureOpenAIApiVersion parameter to specify the API version.
If you were using Azure Managed Identity, you now need to use the azureADTokenProvider parameter to the constructor instead of credentials, see the Azure Managed Identity section for more details.
If you were using environment variables, you now have to set the AZURE_OPENAI_API_INSTANCE_NAME environment variable instead of AZURE_OPENAI_API_ENDPOINT, and add the AZURE_OPENAI_API_VERSION environment variable to specify the API version.