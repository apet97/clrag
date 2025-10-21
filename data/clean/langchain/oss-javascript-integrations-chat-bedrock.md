---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-integrations-chat-bedrock",
  "h1": "oss-javascript-integrations-chat-bedrock",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.482833",
  "sha256_raw": "ed8efe0c4fe077da84c7699030dde06de4682805d61da215a647b4b59ddef489"
}
---

# oss-javascript-integrations-chat-bedrock

> Source: https://docs.langchain.com/oss/javascript/integrations/chat/bedrock

Amazon Bedrock is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies like AI21 Labs, Anthropic, Cohere, Meta, Stability AI, and Amazon via a single API, along with a broad set of capabilities you need to build generative AI applications with security, privacy, and responsible AI.This will help you getting started with Amazon Bedrock chat models. For detailed documentation of all BedrockChat features and configurations head to the API reference.
Copy
<Tip>The newer [`ChatBedrockConverse` chat model is now available via the dedicated `@langchain/aws`](/oss/javascript/integrations/chat/bedrock_converse) integration package. Use [tool calling](/oss/javascript/langchain/tools) with more models with this package.</Tip>
To access Bedrock models you’ll need to create an AWS account, set up the Bedrock API service, get an access key ID and secret key, and install the @langchain/community integration package.
Head to the AWS docs to sign up for AWS and setup your credentials. You’ll also need to turn on model access for your account, which you can do by following these instructions.If you want to get automated tracing of your model calls you can also set your LangSmith API key by uncommenting below:
The LangChain BedrockChat integration lives in the @langchain/community package. You’ll also need to install several official AWS packages as peer dependencies:
You can also use BedrockChat in web environments such as Edge functions or Cloudflare Workers by omitting the @aws-sdk/credential-provider-node dependency and using the web entrypoint:
Currently, only Anthropic, Cohere, and Mistral models are supported with the chat model integration. For foundation models from AI21 or Amazon, see the text generation Bedrock variant.There are a few different ways to authenticate with AWS - the below examples rely on an access key, secret access key and region set in your environment variables:
const aiMsg = await llm.invoke([ [ "system", "You are a helpful assistant that translates English to French. Translate the user sentence.", ], ["human", "I love programming."],])aiMsg
Tool calling with Bedrock models works in a similar way to other models, but note that not all Bedrock models support tool calling. Please refer to the AWS model documentation for more information.