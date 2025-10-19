# oss-python-migrate-langchain-v1

> Source: https://docs.langchain.com/oss/python/migrate/langchain-v1

Simplified package
Thelangchain
package namespace has been significantly reduced in v1 to focus on essential building blocks for agents. The streamlined package makes it easier to discover and use the core functionality.
Namespace
| Module | What’s available | Notes |
|---|---|---|
langchain.agents | create_agent , AgentState | Core agent creation functionality |
langchain.messages | Message types, content blocks, trim_messages | Re-exported from langchain-core |
langchain.tools | @tool , BaseTool , injection helpers | Re-exported from langchain-core |
langchain.chat_models | init_chat_model , BaseChatModel | Unified model initialization |
langchain.embeddings | init_embeddings , Embeddings | Embedding models |
langchain-classic
If you were using any of the following from the langchain
package, you’ll need to install langchain-classic
and update your imports:
- Legacy chains (
LLMChain
,ConversationChain
, etc.) - The indexing API
langchain-community
re-exports- Other deprecated functionality
Migrate to create_agent
Prior to v1.0, we recommended using langgraph.prebuilt.create_react_agent
to build agents.
Now, we recommend you use langchain.agents.create_agent
to build agents.
The table below outlines what functionality has changed from create_react_agent
to create_agent
:
| Section | TL;DR - What’s changed |
|---|---|
| Import path | Package moved from langgraph.prebuilt to langchain.agents |
| Prompts | Parameter renamed to system_prompt , dynamic prompts use middleware |
| Pre-model hook | Replaced by middleware with before_model method |
| Post-model hook | Replaced by middleware with after_model method |
| Custom state | TypedDict only, can be defined via state_schema or middleware |
| Model | Dynamic selection via middleware, pre-bound models not supported |
| Tools | Tool error handling moved to middleware with wrap_tool_call |
| Structured output | prompted output removed, use ToolStrategy /ProviderStrategy |
| Streaming node name | Node name changed from "agent" to "model" |
| Runtime context | Dependency injection via context argument instead of config["configurable"] |
| Namespace | Streamlined to focus on agent building blocks, legacy code moved to langchain-classic |
Import path
The import path for the agent prebuilt has changed fromlanggraph.prebuilt
to langchain.agents
.
The name of the function has changed from create_react_agent
to create_agent
:
Prompts
Static prompt rename
Theprompt
parameter has been renamed to system_prompt
:
SystemMessage
to string
If using SystemMessage
objects in the system prompt, extract the string content:
Dynamic prompts
Dynamic prompts are a core context engineering pattern— they adapt what you tell the model based on the current conversation state. To do this, use the@dynamic_prompt
decorator:
Pre-model hook
Pre-model hooks are now implemented as middleware with thebefore_model
method.
This new pattern is more extensible—you can define multiple middlewares to run before the model is called,
reusing common patterns across different agents.
Common use cases include:
- Summarizing conversation history
- Trimming messages
- Input guardrails, like PII redaction
Post-model hook
Post-model hooks are now implemented as middleware with theafter_model
method.
This new pattern is more extensible—you can define multiple middlewares to run after the model is called,
reusing common patterns across different agents.
Common use cases include:
- Human in the loop
- Output guardrails
Custom state
Custom state extends the default agent state with additional fields. You can define custom state in two ways:- Via
state_schema
oncreate_agent
- Best for state used in tools - Via middleware - Best for state managed by specific middleware hooks and tools attached to said middleware
Defining custom state via middleware is preferred over defining it via
state_schema
on create_agent
because it allows you to keep state extensions conceptually scoped to the relevant middleware and tools.state_schema
is still supported for backwards compatibility on create_agent
.Defining state via state_schema
Use the state_schema
parameter when your custom state needs to be accessed by tools:
Defining state via middleware
Middleware can also define custom state by setting thestate_schema
attribute.
This helps to keep state extensions conceptually scoped to the relevant middleware and tools.
State type restrictions
create_agent
only supports TypedDict
for state schemas. Pydantic models and dataclasses are no longer supported.
langchain.agents.AgentState
instead of BaseModel
or decorating with dataclass
.
If you need to perform validation, handle it in middleware hooks instead.
Model
Dynamic model selection allows you to choose different models based on runtime context (e.g., task complexity, cost constraints, or user preferences).create_react_agent
released in v0.6 of langgraph-prebuilt
supported dynamic model and tool selection
via a callable passed to the model
parameter.
This functionality has been ported to the middleware interface in v1.
Dynamic model selection
Pre-bound models
To better support structured output,create_agent
no longer accepts pre-bound models with tools or configuration:
Dynamic model functions can return pre-bound models if structured output is not used.
Tools
Thetools
argument to create_agent
accepts a list of:
- LangChain
BaseTool
instances (functions decorated with@tool
) - Callable objects (functions) with proper type hints and a docstring
dict
that represents a built-in provider tools
ToolNode
instances.
Handling tool errors
You can now configure the handling of tool errors with middleware implementing thewrap_tool_call
method.
Structured output
Node changes
Structured output used to be generated in a separate node from the main agent. This is no longer the case. We generate structured output in the main loop, reducing cost and latency.Tool and provider strategies
In v1, there are two new structured output strategies:ToolStrategy
uses artificial tool calling to generate structured outputProviderStrategy
uses provider-native structured output generation
Prompted output removed
Prompted output is no longer supported via theresponse_format
argument. Compared to strategies
like artificial tool calling and provider native structured output, prompted output has not proven to be particularly reliable.
Streaming node name rename
When streaming events from agents, the node name has changed from"agent"
to "model"
to better reflect the node’s purpose.
Runtime context
When you invoke an agent, it’s often the case that you want to pass two types of data:- Dynamic state that changes throughout the conversation (e.g., message history)
- Static context that doesn’t change during the conversation (e.g., user metadata)
context
parameter to invoke
and stream
.
The old
config["configurable"]
pattern still works for backward compatibility, but using the new context
parameter is recommended for new applications or applications migrating to v1.Standard content
In v1, messages gain provider-agnostic standard content blocks. Access them via @[message.content_blocks
][content_blocks] for a consistent, typed view across providers. The existing message.content
field remains unchanged for strings or provider-native structures.
What changed
- New
content_blocks
property on messages for normalized content - Standardized block shapes, documented in Messages
- Optional serialization of standard blocks into
content
viaLC_OUTPUT_VERSION=v1
oroutput_version="v1"
Read standardized content
Create multimodal messages
Example block shapes
Serialize standard content
Standard content blocks are not serialized into thecontent
attribute by default. If you need to access standard content blocks in the content
attribute (e.g., when sending messages to a client), you can opt-in to serializing them into content
.
Simplified package
Thelangchain
package namespace has been significantly reduced in v1 to focus on essential building blocks for agents. The streamlined package makes it easier to discover and use the core functionality.
Namespace
| Module | What’s available | Notes |
|---|---|---|
langchain.agents | create_agent , AgentState | Core agent creation functionality |
langchain.messages | Message types, content blocks, trim_messages | Re-exported from langchain-core |
langchain.tools | @tool , BaseTool , injection helpers | Re-exported from langchain-core |
langchain.chat_models | init_chat_model , BaseChatModel | Unified model initialization |
langchain.embeddings | init_embeddings , Embeddings | Embedding models |
langchain-classic
If you were using any of the following from the langchain
package, you’ll need to install langchain-classic
and update your imports:
- Legacy chains (
LLMChain
,ConversationChain
, etc.) - The indexing API
langchain-community
re-exports- Other deprecated functionality
Breaking changes
Dropped Python 3.9 support
All LangChain packages now require Python 3.10 or higher. Python 3.9 reaches end of life in October 2025.Updated return type for chat models
The return type signature for chat model invocation has been fixed fromBaseMessage
to AIMessage
. Custom chat models implementing bind_tools
should update their return signature:
Default message format for OpenAI Responses API
When interacting with the Responses API,langchain-openai
now defaults to storing response items in message content
. To restore previous behavior, set the LC_OUTPUT_VERSION
environment variable to v0
, or specify output_version="v0"
when instantiating ChatOpenAI
.
Default max_tokens
in langchain-anthropic
The max_tokens
parameter in langchain-anthropic
now defaults to higher values based on the model chosen, rather than the previous default of 1024
. If you relied on the old default, explicitly set max_tokens=1024
.
Legacy code moved to langchain-classic
Existing functionality outside the focus of standard interfaces and agents has been moved to the langchain-classic
package. See the Simplified namespace section for details on what’s available in the core langchain
package and what moved to langchain-classic
.
Removal of deprecated APIs
Methods, functions, and other objects that were already deprecated and slated for removal in 1.0 have been deleted. Check the deprecation notices from previous versions for replacement APIs..text()
is now a property
Use of the .text()
method on message objects should drop the parentheses:
.text()
) will continue to function but now emit a warning.