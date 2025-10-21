---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langchain-agents",
  "h1": "oss-javascript-langchain-agents",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.445148",
  "sha256_raw": "da22aaa3a12c32c179d302aff64615c7092ab58d17bc9e43115a611b760df392"
}
---

# oss-javascript-langchain-agents

> Source: https://docs.langchain.com/oss/javascript/langchain/agents

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
createAgent()
provides a production-ready agent implementation.
An LLM Agent runs tools in a loop to achieve a goal.
An agent runs until a stop condition is met - i.e., when the model emits a final output or an iteration limit is reached.
createAgent()
builds a graph-based agent runtime using LangGraph. A graph consists of nodes (steps) and edges (connections) that define how your agent processes information. The agent moves through this graph, executing nodes like the model node (which calls the model), the tools node (which executes tools), or middleware.Learn more about the Graph API.Core components
Model
The model is the reasoning engine of your agent. It can be specified in multiple ways, supporting both static and dynamic model selection.Static model
Static models are configured once when creating the agent and remain unchanged throughout execution. This is the most common and straightforward approach. To initialize a static model from a :provider:model
(e.g. "openai:gpt-5"
). You may want more control over the model configuration, in which case you can initialize a model instance directly using the provider package:
temperature
, max_tokens
, timeouts
, or configure API keys, base_url
, and other provider-specific settings. Refer to the API reference to see available params and methods on your model.
Dynamic model
Dynamic models are selected at based on the current and context. This enables sophisticated routing logic and cost optimization. To use a dynamic model, create middleware withwrapModelCall
that modifies the model in the request:
Tools
Tools give agents the ability to take actions. Agents go beyond simple model-only tool binding by facilitating:- Multiple tool calls in sequence (triggered by a single prompt)
- Parallel tool calls when appropriate
- Dynamic tool selection based on previous results
- Tool retry logic and error handling
- State persistence across tool calls
Defining tools
Pass a list of tools to the agent.Tool error handling
To customize how tool errors are handled, use thewrapToolCall
hook in a custom middleware:
ToolMessage
] with the custom error message when a tool fails.
Tool use in the ReAct loop
Agents follow the ReAct (“Reasoning + Acting”) pattern, alternating between brief reasoning steps with targeted tool calls and feeding the resulting observations into subsequent decisions until they can deliver a final answer.Example of ReAct loop
Example of ReAct loop
Prompt: Identify the current most popular wireless headphones and verify availability.
- Reasoning: “Popularity is time-sensitive, I need to use the provided search tool.”
- Acting: Call
search_products("wireless headphones")
- Reasoning: “I need to confirm availability for the top-ranked item before answering.”
- Acting: Call
check_inventory("WH-1000XM5")
- Reasoning: “I have the most popular model and its stock status. I can now answer the user’s question.”
- Acting: Produce final answer
System prompt
You can shape how your agent approaches tasks by providing a prompt. The @[system_prompt
] parameter can be provided as a string:
system_prompt
] is provided, the agent will infer its task from the messages directly.
Dynamic system prompt
For more advanced use cases where you need to modify the system prompt based on runtime context or agent state, you can use middleware.Invocation
You can invoke an agent by passing an update to its state. All agents include a sequence of messages in their state; to invoke the agent, pass a new message:Advanced concepts
Structured output
In some situations, you may want the agent to return an output in a specific format. LangChain provides a simple, universal way to do this with theresponseFormat
parameter.
Memory
Agents maintain conversation history automatically through the message state. You can also configure the agent to use a custom state schema to remember additional information during the conversation. Information stored in the state can be thought of as the short-term memory of the agent:Streaming
We’ve seen how the agent can be called withinvoke
to get a final response. If the agent executes multiple steps, this may take a while. To show intermediate progress, we can stream back messages as they occur.
Middleware
Middleware provides powerful extensibility for customizing agent behavior at different stages of execution. You can use middleware to:- Process state before the model is called (e.g., message trimming, context injection)
- Modify or validate the model’s response (e.g., guardrails, content filtering)
- Handle tool execution errors with custom logic
- Implement dynamic model selection based on state or context
- Add custom logging, monitoring, or analytics