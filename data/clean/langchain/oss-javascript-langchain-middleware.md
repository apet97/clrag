---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langchain-middleware",
  "h1": "oss-javascript-langchain-middleware",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.487189",
  "sha256_raw": "c38453b8eae6ab2fac1bbc21ff884c1438705f5c9493725887fee33b37142c03"
}
---

# oss-javascript-langchain-middleware

> Source: https://docs.langchain.com/oss/javascript/langchain/middleware

What can middleware do?
Monitor
Modify
Control
Enforce
create_agent
]:
Built-in middleware
LangChain provides prebuilt middleware for common use cases:Summarization
Automatically summarize conversation history when approaching token limits.- Long-running conversations that exceed context windows
- Multi-turn dialogues with extensive history
- Applications where preserving full conversation context matters
Configuration options
Configuration options
Human-in-the-loop
Pause agent execution for human approval, editing, or rejection of tool calls before they execute.- High-stakes operations requiring human approval (database writes, financial transactions)
- Compliance workflows where human oversight is mandatory
- Long running conversations where human feedback is used to guide the agent
Configuration options
Configuration options
Anthropic prompt caching
Reduce costs by caching repetitive prompt prefixes with Anthropic models.- Applications with long, repeated system prompts
- Agents that reuse the same context across invocations
- Reducing API costs for high-volume deployments
Configuration options
Configuration options
Model call limit
Limit the number of model calls to prevent infinite loops or excessive costs.- Preventing runaway agents from making too many API calls
- Enforcing cost controls on production deployments
- Testing agent behavior within specific call budgets
Configuration options
Configuration options
Tool call limit
Limit the number of tool calls to specific tools or all tools.- Preventing excessive calls to expensive external APIs
- Limiting web searches or database queries
- Enforcing rate limits on specific tool usage
Configuration options
Configuration options
Model fallback
Automatically fallback to alternative models when the primary model fails.- Building resilient agents that handle model outages
- Cost optimization by falling back to cheaper models
- Provider redundancy across OpenAI, Anthropic, etc.
Configuration options
Configuration options
PII detection
Detect and handle Personally Identifiable Information in conversations.- Healthcare and financial applications with compliance requirements
- Customer service agents that need to sanitize logs
- Any application handling sensitive user data
Configuration options
Configuration options
email
, credit_card
, ip
, mac_address
, url
) or a custom type name."block"
- Throw error when detected"redact"
- Replace with[REDACTED_TYPE]
"mask"
- Partially mask (e.g.,****-****-****-1234
)"hash"
- Replace with deterministic hash
Planning
Add todo list management capabilities for complex multi-step tasks.write_todos
tool and system prompts to guide effective task planning.Configuration options
Configuration options
LLM tool selector
Use an LLM to intelligently select relevant tools before calling the main model.- Agents with many tools (10+) where most aren’t relevant per query
- Reducing token usage by filtering irrelevant tools
- Improving model focus and accuracy
Configuration options
Configuration options
Context editing
Manage conversation context by trimming, summarizing, or clearing tool uses.- Long conversations that need periodic context cleanup
- Removing failed tool attempts from context
- Custom context management strategies
Configuration options
Configuration options
Custom middleware
Build custom middleware by implementing hooks that run at specific points in the agent execution flow.Class-based middleware
Two hook styles
Node-style hooks
Wrap-style hooks
Node-style hooks
Run at specific points in the execution flow:beforeAgent
- Before agent starts (once per invocation)beforeModel
- Before each model callafterModel
- After each model responseafterAgent
- After agent completes (up to once per invocation)
Wrap-style hooks
Intercept execution and control when the handler is called:wrapModelCall
- Around each model callwrapToolCall
- Around each tool call
Custom state schema
Middleware can extend the agent’s state with custom properties. Define a custom state type and set it as thestate_schema
:
Context extension
Context properties are configuration values passed through the runnable config. Unlike state, context is read-only and typically used for configuration that doesn’t change during execution. Middleware can define context requirements that must be satisfied through the agent’s configuration:Execution order
When using multiple middleware, understanding execution order is important:Execution flow (click to expand)
Execution flow (click to expand)
middleware1.before_agent()
middleware2.before_agent()
middleware3.before_agent()
middleware1.before_model()
middleware2.before_model()
middleware3.before_model()
middleware1.wrap_model_call()
→middleware2.wrap_model_call()
→middleware3.wrap_model_call()
→ model
middleware3.after_model()
middleware2.after_model()
middleware1.after_model()
middleware3.after_agent()
middleware2.after_agent()
middleware1.after_agent()
before_*
hooks: First to lastafter_*
hooks: Last to first (reverse)wrap_*
hooks: Nested (first middleware wraps all others)
Agent jumps
To exit early from middleware, return a dictionary withjump_to
:
"end"
: Jump to the end of the agent execution"tools"
: Jump to the tools node"model"
: Jump to the model node (or the firstbefore_model
hook)
before_model
or after_model
, jumping to "model"
will cause all before_model
middleware to run again.
To enable jumping, decorate your hook with @hook_config(can_jump_to=[...])
:
Best practices
- Keep middleware focused - each should do one thing well
- Handle errors gracefully - don’t let middleware errors crash the agent
- Use appropriate hook types:
- Node-style for sequential logic (logging, validation)
- Wrap-style for control flow (retry, fallback, caching)
- Clearly document any custom state properties
- Unit test middleware independently before integrating
- Consider execution order - place critical middleware first in the list
- Use built-in middleware when possible, don’t reinvent the wheel :)
Examples
Dynamically selecting tools
Select relevant tools at runtime to improve performance and accuracy.- Shorter prompts - Reduce complexity by exposing only relevant tools
- Better accuracy - Models choose correctly from fewer options
- Permission control - Dynamically filter tools based on user access
Additional resources
- Middleware API reference - Complete guide to custom middleware
- Human-in-the-loop - Add human review for sensitive operations
- Testing agents - Strategies for testing safety mechanisms