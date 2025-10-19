# oss-python-langchain-structured-output

> Source: https://docs.langchain.com/oss/python/langchain/structured-output

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
create_agent
handles structured output automatically. The user sets their desired structured output schema, and when the model generates the structured data, it’s captured, validated, and returned in the 'structured_response'
key of the agent’s state.
Response Format
Controls how the agent returns structured data:ToolStrategy[StructuredResponseT]
: Uses tool calling for structured outputProviderStrategy[StructuredResponseT]
: Uses provider-native structured outputtype[StructuredResponseT]
: Schema type - automatically selects best strategy based on model capabilitiesNone
: No structured output
ProviderStrategy
for models supporting native structured output (OpenAI, Grok)ToolStrategy
for all other models
structured_response
key of the agent’s final state.
Provider strategy
Some model providers support structured output natively through their APIs (currently only OpenAI and Grok). This is the most reliable method when available. To use this strategy, configure aProviderStrategy
:
The schema defining the structured output format. Supports:
- Pydantic models:
BaseModel
subclasses with field validation - Dataclasses: Python dataclasses with type annotations
- TypedDict: Typed dictionary classes
- JSON Schema: Dictionary with JSON schema specification
ProviderStrategy
when you pass a schema type directly to create_agent.response_format
and the model supports native structured output:
If the provider natively supports structured output for your model choice, it is functionally equivalent to write
response_format=ProductReview
instead of response_format=ToolStrategy(ProductReview)
. In either case, if structured output is not supported, the agent will fall back to a tool calling strategy.Tool calling strategy
For models that don’t support native structured output, LangChain uses tool calling to achieve the same result. This works with all models that support tool calling, which is most modern models. To use this strategy, configure aToolStrategy
:
The schema defining the structured output format. Supports:
- Pydantic models:
BaseModel
subclasses with field validation - Dataclasses: Python dataclasses with type annotations
- TypedDict: Typed dictionary classes
- JSON Schema: Dictionary with JSON schema specification
- Union types: Multiple schema options. The model will choose the most appropriate schema based on the context.
Custom content for the tool message returned when structured output is generated.
If not provided, defaults to a message showing the structured response data.
Error handling strategy for structured output validation failures. Defaults to
True
.True
: Catch all errors with default error templatestr
: Catch all errors with this custom messagetype[Exception]
: Only catch this exception type with default messagetuple[type[Exception], ...]
: Only catch these exception types with default messageCallable[[Exception], str]
: Custom function that returns error messageFalse
: No retry, let exceptions propagate
Custom tool message content
Thetool_message_content
parameter allows you to customize the message that appears in the conversation history when structured output is generated:
tool_message_content
, our final ToolMessage
would be:
Error handling
Models can make mistakes when generating structured output via tool calling. LangChain provides intelligent retry mechanisms to handle these errors automatically.Multiple structured outputs error
When a model incorrectly calls multiple structured output tools, the agent provides error feedback in aToolMessage
and prompts the model to retry:
Schema validation error
When structured output doesn’t match the expected schema, the agent provides specific error feedback:Error handling strategies
You can customize how errors are handled using thehandle_errors
parameter:
Custom error message:
handle_errors
is a string, the agent will always prompt the model to re-try with a fixed tool message:
handle_errors
is an exception type, the agent will only retry (using the default error message) if the exception raised is the specified type. In all other cases, the exception will be raised.
Handle multiple exception types:
handle_errors
is a tuple of exceptions, the agent will only retry (using the default error message) if the exception raised is one of the specified types. In all other cases, the exception will be raised.
Custom error handler function:
StructuredOutputValidationError
:
MultipleStructuredOutputsError
: