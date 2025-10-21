---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langchain-models",
  "h1": "oss-python-langchain-models",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.459595",
  "sha256_raw": "f47d376fd2ed722be4b2a6da84b1f4f70955c29ebbeb85cbdfb93eeb00578299"
}
---

# oss-python-langchain-models

> Source: https://docs.langchain.com/oss/python/langchain/models

- Tool calling - calling external tools (like databases queries or API calls) and use results in their responses.
- Structured output - where the model’s response is constrained follow a defined format.
- Multimodality - process and return data other than text, such as images, audio, and video.
- Reasoning - models perform multi-step reasoning to arrive at a conclusion.
Basic usage
Models can be utilized in two ways:- With agents - Models can be dynamically specified when creating an agent. See the agents guide for more details on how to do this.
- Standalone - Models can be called directly (outside of the agent loop) for tasks like text generation, classification, or extraction without the need for an agent framework.
Initialize a model
The easiest way to get started with a standalone model in LangChain is to useinit_chat_model
to initialize one from a provider of your choice (examples below):
init_chat_model
for more detail, including information on how to pass model parameters.
Key methods
Invoke
Stream
Batch
Parameters
A chat model takes parameters that can be used to configure its behavior. The full set of supported parameters varies by model and provider, but standard ones include:init_chat_model
, pass these parameters as inline :
ChatOpenAI
has use_responses_api
to dictate whether to use the OpenAI Responses or Completions API.To find all the parameters supported by a given chat model, head to the chat model integrations page.Invocation
A chat model must be invoked to generate an output. There are three primary invocation methods, each suited to different use cases.Invoke
The most straightforward way to call a model is to useinvoke()
with a single message or a list of messages.
Stream
Most models can stream their output content while it is being generated. By displaying output progressively, streaming significantly improves user experience, particularly for longer responses. Callingstream()
returns an that yields output chunks as they are produced. You can use a loop to process each chunk in real-time:
invoke()
, which returns a single AIMessage
after the model has finished generating its full response, stream()
returns multiple AIMessageChunk
objects, each containing a portion of the output text. Importantly, each chunk in a stream is designed to be gathered into a full message via summation:
invoke()
- for example, it can be aggregated into a message history and passed back to the model as conversational context.
Advanced streaming topics
Advanced streaming topics
"Auto-streaming" chat models
"Auto-streaming" chat models
model.invoke()
within nodes, but LangChain will automatically delegate to streaming if running in a streaming mode.How it works
When youinvoke()
a chat model, LangChain will automatically switch to an internal streaming mode if it detects that you are trying to stream the overall application. The result of the invocation will be the same as far as the code that was using invoke is concerned; however, while the chat model is being streamed, LangChain will take care of invoking on_llm_new_token
events in LangChain’s callback system.Callback events allow LangGraph stream()
and astream_events()
to surface the chat model’s output in real-time.Streaming events
Streaming events
astream_events()
.This simplifies filtering based on event types and other metadata, and will aggregate the full message in the background. See below for an example.Batch
Batching a collection of independent requests to a model can significantly improve performance and reduce costs, as the processing can be done in parallel:batch()
will only return the final output for the entire batch. If you want to receive the output for each individual input as it finishes generating, you can stream results with batch_as_completed()
:
batch()
or batch_as_completed()
, you may want to control the maximum number of parallel calls. This can be done by setting the max_concurrency
attribute in the RunnableConfig
dictionary.RunnableConfig
reference for a full list of supported attributes.Tool calling
Models can request to call tools that perform tasks such as fetching data from a database, searching the web, or running code. Tools are pairings of:- A schema, including the name of the tool, a description, and/or argument definitions (often a JSON schema)
- A function or to execute.
bind_tools()
. In subsequent invocations, the model can choose to call any of the bound tools as needed.
Some model providers offer built-in tools that can be enabled via model or invocation parameters (e.g. ChatOpenAI
, ChatAnthropic
). Check the respective provider reference for details.
Tool execution loop
Tool execution loop
ToolMessage
returned by the tool includes a tool_call_id
that matches the original tool call, helping the model correlate results with requests.Forcing tool calls
Forcing tool calls
Parallel tool calls
Parallel tool calls
Streaming tool calls
Streaming tool calls
ToolCallChunk
. This allows you to see tool calls as they’re being generated rather than waiting for the complete response.Structured outputs
Models can be requested to provide their response in a format matching a given schema. This is useful for ensuring the output can be easily parsed and used in subsequent processing. LangChain supports multiple schema types and methods for enforcing structured outputs.- Pydantic
- TypedDict
- JSON Schema
- Method parameter: Some providers support different methods (
'json_schema'
,'function_calling'
,'json_mode'
)'json_schema'
typically refers to dedicated structured output features offered by a provider'function_calling'
derives structured output by forcing a tool call following the given schema'json_mode'
is a precursor to'json_schema'
offered by some providers- it generates valid json, but the schema must be described in the prompt
- Include raw: Use
include_raw=True
to get both the parsed output and the raw AI message - Validation: Pydantic models provide automatic validation, while
TypedDict
and JSON Schema require manual validation
Example: Message output alongside parsed structure
Example: Message output alongside parsed structure
AIMessage
object alongside the parsed representation to access response metadata such as token counts. To do this, set include_raw=True
when calling with_structured_output
:Example: Nested structures
Example: Nested structures
Supported models
LangChain supports all major model providers, including OpenAI, Anthropic, Google, Azure, AWS Bedrock, and more. Each provider offers a variety of models with different capabilities. For a full list of supported models in LangChain, see the integrations page.Advanced topics
Multimodal
Certain models can process and return non-textual data such as images, audio, and video. You can pass non-textual data to a model by providing content blocks.- Data in the cross-provider standard format (see our messages guide)
- OpenAI chat completions format
- Any format that is native to that specific provider (e.g., Anthropic models accept Anthropic native format)
AIMessage
will have content blocks with multimodal types.
Reasoning
Newer models are capable of performing multi-step reasoning to arrive at a conclusion. This involves breaking down complex problems into smaller, more manageable steps. If supported by the underlying model, you can surface this reasoning process to better understand how the model arrived at its final answer.'low'
or 'high'
) or integer token budgets.
For details, see the integrations page or reference for your respective chat model.
Local models
LangChain supports running models locally on your own hardware. This is useful for scenarios where either data privacy is critical, you want to invoke a custom model, or when you want to avoid the costs incurred when using a cloud-based model. Ollama is one of the easiest ways to run models locally. See the full list of local integrations on the integrations page.Prompt caching
Many providers offer prompt caching features to reduce latency and cost on repeat processing of the same tokens. These features can be implicit or explicit:- Implicit prompt caching: providers will automatically pass on cost savings if a request hits a cache. Examples: OpenAI and Gemini (Gemini 2.5 and above).
- Explicit caching: providers allow you to manually indicate cache points for greater control or to guarantee cost savings. Examples:
ChatOpenAI
(viaprompt_cache_key
), Anthropic, AWS Bedrock, Gemini.
Server-side tool use
Some providers support server-side tool-calling loops: models can interact with web search, code interpreters, and other tools and analyze the results in a single conversational turn. If a model invokes a tool server-side, the content of the response message will include content representing the invocation and result of the tool. Accessing the content blocks of the response will return the server-side tool calls and results in a provider-agnostic format:Rate limiting
Many chat model providers impose a limit on the number of invocations that can be made in a given time period. If you hit a rate limit, you will typically receive a rate limit error response from the provider, and will need to wait before making more requests. To help manage rate limits, chat model integrations accept arate_limiter
parameter that can be provided during initialization to control the rate at which requests are made.
Initialize and use a rate limiter
Initialize and use a rate limiter
InMemoryRateLimiter
. This limiter is thread safe and can be shared by multiple threads in the same process.Base URL or proxy
For many chat model integrations, you can configure the base URL for API requests, which allows you to use model providers that have OpenAI-compatible APIs or to use a proxy server.Base URL
Base URL
Proxy configuration
Proxy configuration
Log probabilities
Certain models can be configured to return token-level log probabilities representing the likelihood of a given token by setting thelogprobs
parameter when initializing the model:
Token usage
A number of model providers return token usage information as part of the invocation response. When available, this information will be included on theAIMessage
objects produced by the corresponding model. For more details, see the messages guide.
- Callback handler
- Context manager
Invocation config
When invoking a model, you can pass additional configuration through theconfig
parameter using a RunnableConfig
dictionary. This provides run-time control over execution behavior, callbacks, and metadata tracking.
Common configuration options include:
- Debugging with LangSmith tracing
- Implementing custom logging or monitoring
- Controlling resource usage in production
- Tracking invocations across complex pipelines
Key configuration attributes
Key configuration attributes
Configurable models
You can also create a runtime-configurable model by specifyingconfigurable_fields
. If you don’t specify a model value, then 'model'
and 'model_provider'
will be configurable by default.
Configurable model with default values
Configurable model with default values
Using a configurable model declaratively
Using a configurable model declaratively
bind_tools
, with_structured_output
, with_configurable
, etc. on a configurable model and chain a configurable model in the same way that we would a regularly instantiated chat model object.