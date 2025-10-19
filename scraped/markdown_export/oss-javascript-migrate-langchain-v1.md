# oss-javascript-migrate-langchain-v1

> Source: https://docs.langchain.com/oss/javascript/migrate/langchain-v1

createAgent
In v1, the react agent prebuilt is now in the langchain package. The table below outlines what functionality has changed:
| Section | What changed |
|---|---|
| Import path | Package moved from @langchain/langgraph/prebuilts to langchain |
| Prompts | Parameter renamed to systemPrompt , dynamic prompts use middleware |
| Pre-model hook | Replaced by middleware with beforeModel method |
| Post-model hook | Replaced by middleware with afterModel method |
| Custom state | Defined in middleware, zod objects only |
| Model | Dynamic selection via middleware, pre-bound models not supported |
| Tools | Tool error handling moved to middleware with wrapToolCall |
| Structured output | prompted output removed, use toolStrategy /providerStrategy |
| Streaming node name | Node name changed from "agent" to "model" |
| Runtime context | context property instead of config.configurable |
| Namespace | Streamlined to focus on agent building blocks, legacy code moved to @langchain/classic |
Import path
The import path for the react agent prebuilt has changed from@langchain/langgraph/prebuilts
to langchain
. The name of the function has changed from createReactAgent
to createAgent
:
Prompts
Static prompt rename
Theprompt
parameter has been renamed to systemPrompt
:
SystemMessage
If using SystemMessage
objects in the system prompt, the string content is now used directly:
Dynamic prompts
Dynamic prompts are a core context engineering pattern— they adapt what you tell the model based on the current conversation state. To do this, usedynamicSystemPromptMiddleware
:
Pre-model hook
Pre-model hooks are now implemented as middleware with thebeforeModel
method. This pattern is more extensible—you can define multiple middlewares to run before the model is called and reuse them across agents.
Common use cases include:
- Summarizing conversation history
- Trimming messages
- Input guardrails, like PII redaction
Post-model hook
Post-model hooks are now implemented as middleware with theafterModel
method. This lets you compose multiple handlers after the model responds.
Common use cases include:
- Human-in-the-loop approval
- Output guardrails
Custom state
Custom state is now defined in middleware using thestateSchema
property. Use Zod to declare additional state fields that are carried through the agent run.
Model
Dynamic model selection now happens via middleware. UsewrapModelCall
to swap models (and tools) based on state or runtime context. In createReactAgent
, this was done via a function passed to the model
parameter.
This functionality has been ported to the middleware interface in v1.
Dynamic model selection
Pre-bound models
To better support structured output,createAgent
should receive a plain model (string or instance) and a separate tools
list. Avoid passing models pre-bound with tools when using structured output.
Tools
Thetools
argument to createAgent
accepts:
- Functions created with
tool
- LangChain tool instances
- Objects that represent built-in provider tools
wrapToolCall
to centralize error handling and logging for tools.
Structured output
Node changes
Structured output used to be generated in a separate node from the main agent. This is no longer the case. Structured output is generated in the main loop (no extra LLM call), reducing cost and latency.Tool and provider strategies
In v1, there are two strategies:toolStrategy
uses artificial tool calling to generate structured outputproviderStrategy
uses provider-native structured output generation
Prompted output removed
Prompted output via custom instructions inresponseFormat
is removed in favor of the above strategies.
Streaming node name rename
When streaming events from agents, the node name was changed from"agent"
to "model"
to better reflect the node’s purpose.
Runtime context
When invoking an agent, pass static, read-only configuration via thecontext
config argument. This replaces patterns that used config.configurable
.
The old
config.configurable
pattern still works for backward compatibility, but using the new context
parameter is recommended for new applications or applications migrating to v1.Standard content
In v1, messages gain provider-agnostic standard content blocks. Access them viamessage.contentBlocks
for a consistent, typed view across providers. The existing message.content
field remains unchanged for strings or provider-native structures.
What changed
- New
contentBlocks
property on messages for normalized content. - New TypeScript types under
ContentBlock
for strong typing. - Optional serialization of standard blocks into
content
viaLC_OUTPUT_VERSION=v1
oroutputVersion: "v1"
.
Read standardized content
Create multimodal messages
Example block types
Serialize standard content
Standard content blocks are not serialized into thecontent
attribute by default. If you need to access standard content blocks in the content
attribute (e.g., when sending messages to a client), you can opt-in to serializing them into content
.
Simplified package
Thelangchain
package namespace is streamlined to focus on agent building blocks. Legacy functionality has moved to @langchain/classic
. The new package exposes only the most useful and relevant functionality.
Exports
The v1 package includes:| Module | What’s available | Notes |
|---|---|---|
| Agents | createAgent , AgentState | Core agent creation functionality |
| Messages | Message types, content blocks, trimMessages | Re-exported from @langchain/core |
| Tools | tool , tool classes | Re-exported from @langchain/core |
| Chat models | initChatModel , BaseChatModel | Unified model initialization |
@langchain/classic
If you use legacy chains, the indexing API, or functionality previously re-exported from @langchain/community
, install @langchain/classic
and update imports:
Breaking changes
Dropped Node 18 support
All LangChain packages now require Node.js 20 or higher. Node.js 18 reached end of life in March 2025.New build outputs
Builds for all langchain packages now use a bundler based approach instead of using raw typescript outputs. If you were importing files from thedist/
directory (which is not recommended), you will need to update your imports to use the new module system.
Legacy code moved to @langchain/classic
Legacy functionality outside the focus of standard interfaces and agents has been moved to the @langchain/classic
package. See the Simplified package section for details on what’s available in the core langchain
package and what moved to @langchain/classic
.
Removal of deprecated APIs
Methods, functions, and other objects that were already deprecated and slated for removal in 1.0 have been deleted.View removed deprecated APIs
View removed deprecated APIs
The following deprecated APIs have been removed in v1:
Core functionality
TraceGroup
- Use LangSmith tracing insteadBaseDocumentLoader.loadAndSplit
- Use.load()
followed by a text splitterRemoteRunnable
- No longer supported
Prompts
BasePromptTemplate.serialize
and.deserialize
- Use JSON serialization directlyChatPromptTemplate.fromPromptMessages
- UseChatPromptTemplate.fromMessages
Retrievers
BaseRetrieverInterface.getRelevantDocuments
- Use.invoke()
instead
Runnables
Runnable.bind
- Use.bindTools()
or other specific binding methodsRunnable.map
- Use.batch()
insteadRunnableBatchOptions.maxConcurrency
- UsemaxConcurrency
in the config object
Chat models
BaseChatModel.predictMessages
- Use.invoke()
insteadBaseChatModel.predict
- Use.invoke()
insteadBaseChatModel.serialize
- Use JSON serialization directlyBaseChatModel.callPrompt
- Use.invoke()
insteadBaseChatModel.call
- Use.invoke()
instead
LLMs
BaseLLMParams.concurrency
- UsemaxConcurrency
in the config objectBaseLLM.call
- Use.invoke()
insteadBaseLLM.predict
- Use.invoke()
insteadBaseLLM.predictMessages
- Use.invoke()
insteadBaseLLM.serialize
- Use JSON serialization directly
Streaming
createChatMessageChunkEncoderStream
- Use.stream()
method directly
Tracing
BaseTracer.runMap
- Use LangSmith tracing APIsgetTracingCallbackHandler
- Use LangSmith tracinggetTracingV2CallbackHandler
- Use LangSmith tracingLangChainTracerV1
- Use LangSmith tracing
Memory and storage
BaseListChatMessageHistory.addAIChatMessage
- Use.addMessage()
withAIMessage
BaseStoreInterface
- Use specific store implementations
Utilities
getRuntimeEnvironmentSync
- Use asyncgetRuntimeEnvironment()