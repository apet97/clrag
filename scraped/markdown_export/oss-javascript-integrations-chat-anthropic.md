# oss-javascript-integrations-chat-anthropic

> Source: https://docs.langchain.com/oss/javascript/integrations/chat/anthropic

Anthropic is an AI safety and research company. They are the creator of Claude.
This will help you getting started with Anthropic chat models. For detailed documentation of all ChatAnthropic
features and configurations head to the API reference.
Overview
Integration details
Model features
See the links in the table headers below for guides on how to use specific features.
Setup
You’ll need to sign up and obtain an Anthropic API key, and install the @langchain/anthropic
integration package.
Credentials
Head to Anthropic’s website to sign up to Anthropic and generate an API key. Once you’ve done this set the ANTHROPIC_API_KEY
environment variable:
If you want to get automated tracing of your model calls you can also set your LangSmith API key by uncommenting below:
Installation
The LangChain ChatAnthropic
integration lives in the @langchain/anthropic
package:
Instantiation
Now we can instantiate our model object and generate chat completions:
Invocation
Content blocks
One key difference to note between Anthropic models and most others is that the contents of a single Anthropic AIMessage
can either be a single string or a list of content blocks. For example when an Anthropic model calls a tool, the tool invocation is part of the message content (as well as being exposed in the standardized AIMessage.tool_calls
field):
You can pass custom headers in your requests like this:
Prompt caching
Anthropic supports caching parts of your prompt in order to reduce costs for use-cases that require long context. You can cache tools and both entire messages and individual blocks.
The initial request containing one or more blocks or tool definitions with a "cache_control": { "type": "ephemeral" }
field will automatically cache that part of the prompt. This initial caching step will cost extra, but subsequent requests will be billed at a reduced rate. The cache has a lifetime of 5 minutes, but this is refereshed each time the cache is hit.
There is also currently a minimum cacheable prompt length, which varies according to model. You can see this information here.
This currently requires you to initialize your model with a beta header. Here’s an example of caching part of a system message that contains the LangChain conceptual docs:
We can see that there’s a new field called cache_creation_input_tokens
in the raw usage field returned from Anthropic.
If we use the same messages again, we can see that the long text’s input tokens are read from the cache:
You can also cache tools by setting the same "cache_control": { "type": "ephemeral" }
within a tool definition. This currently requires you to bind a tool in Anthropic’s raw tool format Here’s an example:
For more on how prompt caching works, see Anthropic’s docs.
Custom clients
Anthropic models may be hosted on cloud services such as Google Vertex that rely on a different underlying client with the same interface as the primary Anthropic client. You can access these services by providing a createClient
method that returns an initialized instance of an Anthropic client. Here’s an example:
Citations
Anthropic supports a citations feature that lets Claude attach context to its answers based on source material supplied by the user. This source material can be provided either as document content blocks, which describe full documents, or as search results, which describe relevant passages or snippets returned from a retrieval system. When "citations": { "enabled": true }
is included in a query, Claude may generate direct citations to the provided material in its response.
Document example
In this example we pass a plain text document. In the background, Claude automatically chunks the input text into sentences, which are used when generating citations.
Search results example
In this example, we pass in search results as part of our message content. This allows Claude to cite specific passages or snippets from your own retrieval system in its response.
This approach is helpful when you want Claude to cite information from a specific set of knowledge, but you want to bring your own pre-fetched/cached content directly rather than having the model search or retrieve them automatically.
You can also use a tool to provide search results that the model can cite in its responses. This is well suited for RAG (or Retrieval-Augmented Generation) workflows where Claude can decide when and where to retrieve information from. When returning this information as search results, it gives Claude the ability to create citations from the material returned from the tool.
Here’s how you can create a tool that returns search results in the format expected by Anthropic’s citations API:
Learn more about how RAG works in LangChain here
Learn more about tool calling here
Using with text splitters
Anthropic also lets you specify your own splits using custom document types. LangChain text splitters can be used to generate meaningful splits for this purpose. See the below example, where we split the LangChain.js README (a markdown document) and pass it to Claude as context:
Context management
Anthropic supports a context editing feature that will automatically manage the model’s context window (e.g., by clearing tool results).
See Anthropic documentation for details and configuration options.
Context management is supported since @langchain/anthropic@0.3.29
API reference
For detailed documentation of all ChatAnthropic features and configurations head to the API reference.