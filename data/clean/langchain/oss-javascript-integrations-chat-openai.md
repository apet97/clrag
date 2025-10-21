---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-integrations-chat-openai",
  "h1": "oss-javascript-integrations-chat-openai",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.474982",
  "sha256_raw": "2bb8c875a3fd182a05adb2ff800093becd58a4b0acf714e18ffa9810b47640c0"
}
---

# oss-javascript-integrations-chat-openai

> Source: https://docs.langchain.com/oss/javascript/integrations/chat/openai

Overview
Integration details
| Class | Package | Local | Serializable | PY support | Downloads | Version |
|---|---|---|---|---|---|---|
| ChatOpenAI | @langchain/openai | ❌ | ✅ | ✅ |
Model features
See the links in the table headers below for guides on how to use specific features.| Tool calling | Structured output | JSON mode | Image input | Audio input | Video input | Token-level streaming | Token usage | Logprobs |
|---|---|---|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
Setup
To access OpenAI chat models you’ll need to create an OpenAI account, get an API key, and install the@langchain/openai
integration package.
Credentials
Head to OpenAI’s website to sign up for OpenAI and generate an API key. Once you’ve done this set theOPENAI_API_KEY
environment variable:
Installation
The LangChain @[ChatOpenAI
] integration lives in the @langchain/openai
package:
Instantiation
Now we can instantiate our model object and generate chat completions:Invocation
Custom URLs
You can customize the base URL the SDK sends requests to by passing aconfiguration
parameter like this:
configuration
field also accepts other ClientOptions
parameters accepted by the official SDK.
If you are hosting on Azure OpenAI, see the dedicated page instead.
Custom headers
You can specify custom headers in the sameconfiguration
field:
Disabling streaming usage metadata
Some proxies or third-party providers present largely the same API interface as OpenAI, but don’t support the more recently addedstream_options
parameter to return streaming usage. You can use @[ChatOpenAI
] to access these providers by disabling streaming usage like this:
Calling fine-tuned models
You can call fine-tuned OpenAI models by passing in your correspondingmodelName
parameter.
This generally takes the form of ft:{OPENAI_MODEL_NAME}:{ORG_NAME}::{MODEL_ID}
. For example:
Generation metadata
If you need additional information like logprobs or token usage, these will be returned directly in theinvoke
response within the response_metadata
field on the message.
Requires
@langchain/core
version >=0.1.48.Custom Tools
Custom tools support tools with arbitrary string inputs. They can be particularly useful when you expect your string arguments to be long or complex. If you use a model that supports custom tools, you can use the @[ChatOpenAI
] class and the customTool
function to create a custom tool.
strict: true
As of Aug 6, 2024, OpenAI supports a strict
argument when calling tools that will enforce that the tool argument schema is respected by the model. See more.
Requires
@langchain/openai >= 0.2.6
If
strict: true
the tool definition will also be validated, and a subset of JSON schema are accepted. Crucially, schema cannot have optional args (those with default values). Read the full docs on what types of schema are supported.strict: true
argument to .bindTools
will pass the param through to all tool definitions:
Structured output
We can also passstrict: true
to the .withStructuredOutput()
. Here’s an example:
Responses API
CompatibilityThe below points apply to
@langchain/openai>=0.4.5-rc.0
.ChatOpenAI
will route to the Responses API if one of these features is used. You can also specify useResponsesApi: true
when instantiating ChatOpenAI
.
Built-in tools
Equipping @[ChatOpenAI
] with built-in tools will ground its responses with outside information, such as via context in files or the web. The AIMessage generated from the model will include information about the built-in tool invocation.
Web search
To trigger a web search, pass{"type": "web_search_preview"}
to the model as you would another tool.
You can also pass built-in tools as invocation params:
File search
To trigger a file search, pass a file search tool to the model as you would another tool. You will need to populate an OpenAI-managed vector store and include the vector store ID in the tool definition. See OpenAI documentation for more details.Computer Use
ChatOpenAI supports thecomputer-use-preview
model, which is a specialized model for the built-in computer use tool. To enable, pass a computer use tool as you would pass another tool.
Currently tool outputs for computer use are present in AIMessage.additional_kwargs.tool_outputs
. To reply to the computer use tool call, you need to set additional_kwargs.type: "computer_call_output"
while creating a corresponding ToolMessage
.
See OpenAI documentation for more details.
Code interpreter
ChatOpenAI allows you to use the built-in code interpreter tool to support the sandboxed generation and execution of code.Remote MCP
ChatOpenAI supports the built-in remote MCP tool that allows for model-generated calls to MCP servers to happen on OpenAI servers.MCP ApprovalsWhen instructed, OpenAI will request approval before making calls to a remote MCP server.In the above command, we instructed the model to never require approval. We can also configure the model to always request approval, or to always request approval for specific tools:With this configuration, responses can contain tool outputs typed as
mcp_approval_request
. To submit approvals for an approval request, you can structure it into a content block in a followup message:Image Generation
ChatOpenAI allows you to bring the built-in image generation tool to create images as apart of multi-turn conversations through the responses API.Reasoning models
o1
, the default method for withStructuredOutput
is OpenAI’s built-in method for structured output (equivalent to passing method: "jsonSchema"
as an option into withStructuredOutput
). JSON schema mostly works the same as other models, but with one important caveat: when defining schema, z.optional()
is not respected, and you should instead use z.nullable()
.
Here’s an example:
z.nullable()
:
Prompt caching
Newer OpenAI models will automatically cache parts of your prompt if your inputs are above a certain size (1024 tokens at the time of writing) in order to reduce costs for use-cases that require long context. Note: The number of tokens cached for a given query is not yet standardized inAIMessage.usage_metadata
, and is instead contained in the AIMessage.response_metadata
field.
Here’s an example
Predicted output
Some OpenAI models (such as theirgpt-4o
and gpt-4o-mini
series) support Predicted Outputs, which allow you to pass in a known portion of the LLM’s expected output ahead of time to reduce latency. This is useful for cases such as editing text or code, where only a small part of the model’s output will change.
Here’s an example:
Audio output
Some OpenAI models (such asgpt-4o-audio-preview
) support generating audio output. This example shows how to use that feature:
data
field. We are also provided an expires_at
date field. This field represents the date the audio response will no longer be accessible on the server for use in multi-turn conversations.
Streaming Audio Output
OpenAI also supports streaming audio output. Here’s an example:Audio input
These models also support passing audio as input. For this, you must specifyinput_audio
fields as seen below: