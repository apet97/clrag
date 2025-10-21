---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-releases-langchain-v1",
  "h1": "oss-python-releases-langchain-v1",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.455568",
  "sha256_raw": "60ecf0d6dcffdc86c6b6ebe08fcebe03b43d1f2fdf35b8089a45aeac8e2cf68d"
}
---

# oss-python-releases-langchain-v1

> Source: https://docs.langchain.com/oss/python/releases/langchain-v1

create_agent
The new standard for building agents in LangChain, replacing
langgraph.prebuilt.create_react_agent
.Standard content blocks
A new
content_blocks
property that provides unified access to modern LLM features across providers.Simplified namespace
The
langchain
namespace has been streamlined to focus on essential building blocks for agents, with legacy functionality moved to langchain-classic
.create_agent
create_agent
is the standard way to build agents in LangChain 1.0. It provides a simpler interface than langgraph.prebuilt.create_react_agent
while offering greater customization potential by using middleware.
create_agent
is built on the basic agent loop — calling a model, letting it choose tools to execute, and then finishing when it calls no more tools:
For more information, see Agents.
Middleware
Middleware is the defining feature ofcreate_agent
. It offers a highly customizable entry-point, raising the ceiling for what you can build.
Great agents require context engineering: getting the right information to the model at the right time. Middleware helps you control dynamic prompts, conversation summarization, selective tool access, state management, and guardrails through a composable abstraction.
Prebuilt middleware
LangChain provides a few prebuilt middlewares for common patterns, including:PIIMiddleware
: Redact sensitive information before sending to the modelSummarizationMiddleware
: Condense conversation history when it gets too longHumanInTheLoopMiddleware
: Require approval for sensitive tool calls
Custom middleware
You can also build custom middleware to fit your needs. Middleware exposes hooks at each step in an agent’s execution:
Build custom middleware by implementing any of these hooks on a subclass of the
AgentMiddleware
class:
| Hook | When it runs | Use cases |
|---|---|---|
before_agent | Before calling the agent | Load memory, validate input |
before_model | Before each LLM call | Update prompts, trim messages |
wrap_model_call | Around each LLM call | Intercept and modify requests/responses |
wrap_tool_call | Around each tool call | Intercept and modify tool execution |
after_model | After each LLM response | Validate output, apply guardrails |
after_agent | After agent completes | Save results, cleanup |
Built on LangGraph
Becausecreate_agent
is built on LangGraph, you automatically get built in support for long running and reliable agents via:
Persistence
Conversations automatically persist across sessions with built-in checkpointing
Streaming
Stream tokens, tool calls, and reasoning traces in real-time
Human-in-the-loop
Pause agent execution for human approval before sensitive actions
Time travel
Rewind conversations to any point and explore alternate paths and prompts
Structured output
create_agent
has improved structured output generation:
- Main loop integration: Structured output is now generated in the main loop instead of requiring an additional LLM call
- Structured output strategy: Models can choose between calling tools or using provider-side structured output generation
- Cost reduction: Eliminates extra expense from additional LLM calls
handle_errors
parameter to ToolStrategy
:
- Parsing errors: Model generates data that doesn’t match desired structure
- Multiple tool calls: Model generates 2+ tool calls for structured output schemas
Standard content blocks
Content block support is currently only available for the following integrations:Broader support for content blocks will be rolled out gradually across more providers.
content_blocks
property introduces a standard representation for message content that works across providers:
Benefits
- Provider agnostic: Access reasoning traces, citations, built-in tools (web search, code interpreters, etc.), and other features using the same API regardless of provider
- Type safe: Full type hints for all content block types
- Backward compatible: Standard content can be loaded lazily, so there are no associated breaking changes
Simplified package
LangChain v1 streamlines thelangchain
package namespace to focus on essential building blocks for agents. The refined namespace exposes the most useful and relevant functionality:
Namespace
| Module | What’s available | Notes |
|---|---|---|
langchain.agents | create_agent , AgentState | Core agent creation functionality |
langchain.messages | Message types, content blocks, trim_messages | Re-exported from @[langchain-core ] |
langchain.tools | @tool , BaseTool , injection helpers | Re-exported from @[langchain-core ] |
langchain.chat_models | init_chat_model , BaseChatModel | Unified model initialization |
langchain.embeddings | Embeddings , init_embeddings | Embedding models |
langchain-core
for convenience, which gives you a focused API surface for building agents.
langchain-classic
Legacy functionality has moved to langchain-classic
to keep the core packages lean and focused.
What’s in langchain-classic
- Legacy chains and chain implementations
- The indexing API
langchain-community
exports- Other deprecated functionality
langchain-classic
:
Migration guide
See our migration guide for help updating your code to LangChain v1.Reporting issues
Please report any issues discovered with 1.0 on GitHub using the'v1'
label.
Additional resources
LangChain 1.0
Read the announcement
Middleware Guide
Deep dive into middleware
Agents Documentation
Full agent documentation
Message Content
New content blocks API
Migration guide
How to migrate to LangChain v1
GitHub
Report issues or contribute
See also
- Versioning - Understanding version numbers
- Release policy - Detailed release policies