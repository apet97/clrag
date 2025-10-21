---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langchain-context-engineering",
  "h1": "oss-python-langchain-context-engineering",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.478476",
  "sha256_raw": "16b77dc7972df95f452d0321bafd2a34f82e822ce07a59b9022dade82ee49673"
}
---

# oss-python-langchain-context-engineering

> Source: https://docs.langchain.com/oss/python/langchain/context-engineering

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
- The underlying LLM is just not good enough
- The “right” context was not passed to the LLM
The core agent loop
It’s important to understand the core agent loop to understand where context should be accessed and/or updated from. The core agent loop is quite simple:- Get user input
- Call LLM, asking it to either respond or call tools
- If it decides to call tools - then go and execute those tools
- Repeat steps 2 and 3 until it decides to finish
The model
The model (including specific model parameters) that you use is a key part of the agent loop. It drives the whole agent’s reasoning logic. One reason the agent could mess up is the model you are using is just not good enough. In order to build reliable agents, you have to have access to all the possible models. LangChain, with its standard model interfaces, supports this - we have over 50 different provider integrations. Model choice is also related to context engineering, in two ways. First, the way you pass the context to the LLM may depend on what LLM you are using. Some model providers are better at JSON, some at XML. The context engineering you do may be specific to the model choice. Second, the right model to use in the agent loop may depend on the context you want to pass it. As an obvious example - some models have different context windows. If the context in an agent builds up, you may want to use one model provider while the context is small, and then once it gets too large for that model’s context window you may want to switch to another model.Types of context
There are a few different types of context that can be used to construct the context that is ultimately passed to the LLM. Instructions: Base instructions from the developer, commonly referred to as the system prompt. This may be static or dynamic. Tools: What tools the agent has access to. The names and descriptions and arguments of these are just as important as the text in the prompt. Structured output: What format the agent should respond in. The name and description and arguments of these are just as important as the text in the prompt. Session context: We also call this “short term memory” in the docs. In the context of a conversation, this is most easily thought of the list of messages that make up the conversation. But there can often be other, more structured information that you may want the agent to access or update throughout the session. The agent can read and write this context. This context is often put directly into the context that is passed to the LLM. Examples include: messages, files. Long term memory: This is information that should persist across sessions (conversations). Examples include: extracted preferences Runtime configuration context: This is context that is not the “state” or “memory” of the agent, but rather configuration for a given agent run. This is not modified by the agent, and typically isn’t passed into the LLM, but is used to guide the agent’s behavior or look up other context. Examples include: user ID, DB connectionsContext engineering with LangChain
Now we understand the basic agent loop, the importance of the model you use, and the different types of context that exist. Let’s explore the concrete patterns LangChain provides for context engineering.Managing instructions (system prompts)
Static instructions
For fixed instructions that don’t change, use thesystem_prompt
parameter:
Dynamic instructions
For instructions that depend on context (user profile, preferences, session data), use the@dynamic_prompt
middleware:
When to use each:
- Static prompts: Base instructions that never change
- Dynamic prompts: Personalization, A/B testing, context-dependent behavior
Managing conversation context (messages)
Long conversations can exceed context windows or degrade model performance. Use middleware to manage conversation history:Trimming messages
SummarizationMiddleware
which automatically summarizes old messages when approaching token limits.
See Before model hook for more examples.
Contextual tool execution
Tools can access runtime context, session state, and long-term memory to make context-aware decisions:Dynamic tool selection
Control which tools the agent can access based on context, state, or user permissions:Dynamic model selection
Switch models based on conversation complexity, context window needs, or cost optimization:Best practices
- Start simple - Begin with static prompts and tools, add dynamics only when needed
- Test incrementally - Add one context engineering feature at a time
- Monitor performance - Track model calls, token usage, and latency
- Use built-in middleware - Leverage
SummarizationMiddleware
,LLMToolSelectorMiddleware
, etc. - Document your context strategy - Make it clear what context is being passed and why
Related resources
- Middleware - Complete middleware guide
- Tools - Tool creation and context access
- Memory - Short-term and long-term memory patterns
- Agents - Core agent concepts