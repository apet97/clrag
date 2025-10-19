# oss-python-langchain-quickstart

> Source: https://docs.langchain.com/oss/python/langchain/quickstart

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
Tools let a model interact with external systems by calling functions you define.
Tools can depend on runtime context and also interact with agent memory.Notice below how the
get_user_location
tool uses runtime context:Tools should be well-documented: their name, description, and argument names become part of the model’s prompt.
LangChain’s
@tool
decorator adds metadata and enables runtime injection via the ToolRuntime
parameter.4
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