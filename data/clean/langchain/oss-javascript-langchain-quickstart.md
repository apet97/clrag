---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langchain-quickstart",
  "h1": "oss-javascript-langchain-quickstart",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.487520",
  "sha256_raw": "be5c6990ce1f8aa40ebbabd80f0c6b41a18232ac39a292cd08181240edceb8b5"
}
---

# oss-javascript-langchain-quickstart

> Source: https://docs.langchain.com/oss/javascript/langchain/quickstart

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Build a basic agent
Start by creating a simple agent that can answer questions and call tools. The agent will use Claude Sonnet 4.5 as its language model, a basic weather function as a tool, and a simple prompt to guide its behavior.Build a real-world agent
Next, build a practical weather forecasting agent that demonstrates key production concepts:- Detailed system prompts for better agent behavior
- Create tools that integrate with external data
- Model configuration for consistent responses
- Structured output for predictable results
- Conversational memory for chat-like interactions
- Create and run the agent create a fully functional agent
1
Define the system prompt
The system prompt defines your agent’s role and behavior. Keep it specific and actionable:
2
Create tools
Tools are functions your agent can call. Oftentimes tools will want to connect to external systems, and will rely on runtime configuration to do so. Notice here how the
getUserLocation
tool does exactly that:Zod is a library for validating and parsing pre-defined schemas. You can use it to define the input schema for your tools to make sure the agent only calls the tool with the correct arguments.Alternatively, you can define the
schema
property as a JSON schema object. Keep in mind that JSON schemas won’t be validated at runtime.Example: Using JSON schema for tool input
Example: Using JSON schema for tool input
4
Define response format
Optionally, define a structured response format if you need the agent responses to match
a specific schema.
5
6
Create and run the agent
Now assemble your agent with all the components and run it!
- Understand context and remember conversations
- Use multiple tools intelligently
- Provide structured responses in a consistent format
- Handle user-specific information through context
- Maintain conversation state across interactions