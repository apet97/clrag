---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langchain-structured-output",
  "h1": "oss-javascript-langchain-structured-output",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.492388",
  "sha256_raw": "4d4929923ffc6198ef4763b645557c817197e625c41941e88c058c5c59081576"
}
---

# oss-javascript-langchain-structured-output

> Source: https://docs.langchain.com/oss/javascript/langchain/structured-output

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
createAgent
handles structured output automatically. The user sets their desired structured output schema, and when the model generates the structured data, it’s captured, validated, and returned in the structuredResponse
key of the agent’s state.
Response Format
Controls how the agent returns structured data. You can provide either a Zod object or JSON schema. By default, the agent uses a tool calling strategy, in which the output is created by an additional tool call. Certain models support native structured output, in which case the agent will use that strategy instead. You can control the behavior by wrappingResponseFormat
in a toolStrategy
or providerStrategy
function call:
structuredResponse
key of the agent’s final state.
Provider strategy
Some model providers support structured output natively through their APIs (currently only OpenAI and Grok). This is the most reliable method when available. To use this strategy, configure aProviderStrategy
:
The schema defining the structured output format. Supports:
- Zod Schema: A zod schema
- JSON Schema: A JSON schema object
ProviderStrategy
when you pass a schema type directly to createAgent.responseFormat
and the model supports native structured output:
If the provider natively supports structured output for your model choice, it is functionally equivalent to write
responseFormat: contactInfoSchema
instead of responseFormat: toolStrategy(contactInfoSchema)
. In either case, if structured output is not supported, the agent will fall back to a tool calling strategy.Tool calling strategy
For models that don’t support native structured output, LangChain uses tool calling to achieve the same result. This works with all models that support tool calling, which is most modern models. To use this strategy, configure aToolStrategy
:
The schema defining the structured output format. Supports:
- Zod Schema: A zod schema
- JSON Schema: A JSON schema object
Custom content for the tool message returned when structured output is generated.
If not provided, defaults to a message showing the structured response data.
Options parameter containing an optional
handleError
parameter for customizing the error handling strategy.true
: Catch all errors with default error template (default)False
: No retry, let exceptions propagate(error: ToolStrategyError) => string | Promise<string>
: retry with the provided message or throw the error
Custom tool message content
ThetoolMessageContent
parameter allows you to customize the message that appears in the conversation history when structured output is generated:
toolMessageContent
, we’d see:
Error handling
Models can make mistakes when generating structured output via tool calling. LangChain provides intelligent retry mechanisms to handle these errors automatically.Multiple structured outputs error
When a model incorrectly calls multiple structured output tools, the agent provides error feedback in a @[ToolMessage
] and prompts the model to retry:
Schema validation error
When structured output doesn’t match the expected schema, the agent provides specific error feedback:Error handling strategies
You can customize how errors are handled using thehandleErrors
parameter:
Custom error message: