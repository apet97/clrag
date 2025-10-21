---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-releases-langchain-v1",
  "h1": "oss-javascript-releases-langchain-v1",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.432192",
  "sha256_raw": "e2bd6b19c109b97f8107f9273477e00c0b2b9ae9a5674e2076a5460df7970088"
}
---

# oss-javascript-releases-langchain-v1

> Source: https://docs.langchain.com/oss/javascript/releases/langchain-v1

createAgent
A new standard way to build agents in LangChain, replacing
createReactAgent
from LangGraph with a cleaner, more powerful API.Standard content blocks
A new
contentBlocks
property that provides unified access to modern LLM features across all providers.Simplified package
The
langchain
package has been streamlined to focus on essential building blocks for agents, with legacy functionality moved to @langchain/classic
.createAgent
createAgent
is the standard way to build agents in LangChain 1.0. It provides a simpler interface than the prebuilt createReactAgent
exported from LangGraph while offering greater customization potential by using middleware.
createAgent
is built on the basic agent loop — calling a model, letting it choose tools to execute, and then finishing when it calls no more tools:
For more information, see Agents.
Middleware
Middleware is the defining feature ofcreateAgent
. It makes createAgent
highly customizable, raising the ceiling for what you can build.
Great agents require context engineering: getting the right information to the model at the right time. Middleware helps you control dynamic prompts, conversation summarization, selective tool access, state management, and guardrails through a composable abstraction.
Prebuilt middleware
LangChain provides a few prebuilt middlewares for common patterns, including:summarizationMiddleware
: Condense conversation history when it gets too longhumanInTheLoopMiddleware
: Require approval for sensitive tool callspiiRedactionMiddleware
: Redact sensitive information before sending to the model
Custom middleware
You can also build custom middleware to fit your specific needs. Build custom middleware by implementing any of these hooks using thecreateMiddleware
function:
| Hook | When it runs | Use cases |
|---|---|---|
beforeAgent | Before calling the agent | Load memory, validate input |
beforeModel | Before each LLM call | Update prompts, trim messages |
wrapModelCall | Around each LLM call | Intercept and modify requests/responses |
wrapToolCall | Around each tool call | Intercept and modify tool execution |
afterModel | After each LLM response | Validate output, apply guardrails |
afterAgent | After agent completes | Save results, cleanup |
Built on LangGraph
BecausecreateAgent
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
createAgent
has improved structured output generation:
- Main loop integration: Structured output is now generated in the main loop instead of requiring an additional LLM call
- Structured output strategy: Models can choose between calling tools or using provider-side structured output generation
- Cost reduction: Eliminates extra expense from additional LLM calls
handleErrors
parameter to ToolStrategy
:
- Parsing errors: Model generates data that doesn’t match desired structure
- Multiple tool calls: Model generates 2+ tool calls for structured output schemas
Standard content blocks
1.0 releases are available for most packages. Only the following currently support new content blocks:
langchain
@langchain/core
@langchain/anthropic
@langchain/openai
Benefits
- Provider agnostic: Access reasoning traces, citations, built-in tools (web search, code interpreters, etc.), and other features using the same API regardless of provider
- Type safe: Full type hints for all content block types
- Backward compatible: Standard content can be loaded lazily, so there are no associated breaking changes
Simplified package
LangChain v1 streamlines thelangchain
package namespace to focus on essential building blocks for agents. The package exposes only the most useful and relevant functionality:
Most of these are re-exported from @langchain/core
for convenience, which gives you a focused API surface for building agents.
@langchain/classic
Legacy functionality has moved to @langchain/classic
to keep the core package lean and focused.
What’s in @langchain/classic
- Legacy chains and chain implementations
- The indexing API
@langchain/community
exports- Other deprecated functionality
@langchain/classic
:
Reporting issues
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