# oss-javascript-integrations-chat-azure

> Source: https://docs.langchain.com/oss/javascript/integrations/chat/azure

Azure OpenAI is a Microsoft Azure service that provides powerful language models from OpenAI.This will help you getting started with AzureChatOpenAI chat models. For detailed documentation of all AzureChatOpenAI features and configurations head to the API reference.
Azure OpenAI is a cloud service to help you quickly develop generative AI experiences with a diverse set of prebuilt and curated models from OpenAI, Meta and beyond.LangChain.js supports integration with Azure OpenAI using the new Azure integration in the OpenAI SDK.You can learn more about Azure OpenAI and its difference with the OpenAI API on this page.
If you don’t have an Azure account, you can create a free account to get started.You’ll also need to have an Azure OpenAI instance deployed. You can deploy a version on Azure Portal following this guide.Once you have your instance running, make sure you have the name of your instance and key. You can find the key in the Azure Portal, under the “Keys and Endpoint” section of your instance. Then, if using Node.js, you can set your credentials as environment variables:
Now we can instantiate our model object and generate chat completions:
Copy
import { AzureChatOpenAI } from "@langchain/openai"const llm = new AzureChatOpenAI({ model: "gpt-4o", temperature: 0, maxTokens: undefined, maxRetries: 2, azureOpenAIApiKey: process.env.AZURE_OPENAI_API_KEY, // In Node.js defaults to process.env.AZURE_OPENAI_API_KEY azureOpenAIApiInstanceName: process.env.AZURE_OPENAI_API_INSTANCE_NAME, // In Node.js defaults to process.env.AZURE_OPENAI_API_INSTANCE_NAME azureOpenAIApiDeploymentName: process.env.AZURE_OPENAI_API_DEPLOYMENT_NAME, // In Node.js defaults to process.env.AZURE_OPENAI_API_DEPLOYMENT_NAME azureOpenAIApiVersion: process.env.AZURE_OPENAI_API_VERSION, // In Node.js defaults to process.env.AZURE_OPENAI_API_VERSION})
const aiMsg = await llm.invoke([ [ "system", "You are a helpful assistant that translates English to French. Translate the user sentence.", ], ["human", "I love programming."],])aiMsg
If your instance is hosted under a domain other than the default openai.azure.com, you’ll need to use the alternate AZURE_OPENAI_BASE_PATH environment variable.
For example, here’s how you would connect to the domain https://westeurope.api.microsoft.com/openai/deployments/{DEPLOYMENT_NAME}:
Copy
import { AzureChatOpenAI } from "@langchain/openai";const llmWithDifferentDomain = new AzureChatOpenAI({ temperature: 0.9, azureOpenAIApiKey: "<your_key>", // In Node.js defaults to process.env.AZURE_OPENAI_API_KEY azureOpenAIApiDeploymentName: "<your_deployment_name>", // In Node.js defaults to process.env.AZURE_OPENAI_API_DEPLOYMENT_NAME azureOpenAIApiVersion: "<api_version>", // In Node.js defaults to process.env.AZURE_OPENAI_API_VERSION azureOpenAIBasePath: "https://westeurope.api.microsoft.com/openai/deployments", // In Node.js defaults to process.env.AZURE_OPENAI_BASE_PATH});
You can specify custom headers by passing in a configuration field:
Copy
import { AzureChatOpenAI } from "@langchain/openai";const llmWithCustomHeaders = new AzureChatOpenAI({ azureOpenAIApiKey: process.env.AZURE_OPENAI_API_KEY, // In Node.js defaults to process.env.AZURE_OPENAI_API_KEY azureOpenAIApiInstanceName: process.env.AZURE_OPENAI_API_INSTANCE_NAME, // In Node.js defaults to process.env.AZURE_OPENAI_API_INSTANCE_NAME azureOpenAIApiDeploymentName: process.env.AZURE_OPENAI_API_DEPLOYMENT_NAME, // In Node.js defaults to process.env.AZURE_OPENAI_API_DEPLOYMENT_NAME azureOpenAIApiVersion: process.env.AZURE_OPENAI_API_VERSION, // In Node.js defaults to process.env.AZURE_OPENAI_API_VERSION configuration: { defaultHeaders: { "x-custom-header": `SOME_VALUE`, }, },});await llmWithCustomHeaders.invoke("Hi there!");
The configuration field also accepts other ClientOptions parameters accepted by the official SDK.Note: The specific header api-key currently cannot be overridden in this manner and will pass through the value from azureOpenAIApiKey.
If you are using the deprecated Azure OpenAI SDK with the @langchain/azure-openai package, you can update your code to use the new Azure integration following these steps:
Install the new @langchain/openai package and remove the previous @langchain/azure-openai package:
Copy
<Npm2Yarn> @langchain/openai</Npm2Yarn>
Copy
npm uninstall @langchain/azure-openai
Update your imports to use the new @[AzureChatOpenAI] class from the @langchain/openai package:
Copy
import { AzureChatOpenAI } from "@langchain/openai";
Update your code to use the new @[AzureChatOpenAI] class and pass the required parameters:
Copy
const model = new AzureChatOpenAI({ azureOpenAIApiKey: "<your_key>", azureOpenAIApiInstanceName: "<your_instance_name>", azureOpenAIApiDeploymentName: "<your_deployment_name>", azureOpenAIApiVersion: "<api_version>",});
Notice that the constructor now requires the azureOpenAIApiInstanceName parameter instead of the azureOpenAIEndpoint parameter, and adds the azureOpenAIApiVersion parameter to specify the API version.
If you were using Azure Managed Identity, you now need to use the azureADTokenProvider parameter to the constructor instead of credentials, see the Azure Managed Identity section for more details.
If you were using environment variables, you now have to set the AZURE_OPENAI_API_INSTANCE_NAME environment variable instead of AZURE_OPENAI_API_ENDPOINT, and add the AZURE_OPENAI_API_VERSION environment variable to specify the API version.