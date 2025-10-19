# oss-python-langgraph-quickstart

> Source: https://docs.langchain.com/oss/python/langgraph/quickstart

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
- Use the Graph API if you prefer to define your agent as a graph of nodes and edges.
- Use the Functional API if you prefer to define your agent as a single function.
- Use the Graph API
- Use the Functional API
1. Define tools and model
In this example, we’ll use the Claude Sonnet 4.5 model and define tools for addition, multiplication, and division.2. Define state
The graph’s state is used to store the messages and the number of LLM calls.State in LangGraph persists throughout the agent’s execution. The
Annotated
type with operator.add
ensures that new messages are appended to the existing list rather than replacing it.3. Define model node
The model node is used to call the LLM and decide whether to call a tool or not.4. Define tool node
The tool node is used to call the tools and return the results.5. Define end logic
The conditional edge function is used to route to the tool node or end based upon whether the LLM made a tool call.6. Build and compile the agent
The agent is built using theStateGraph
class and compiled using the compile
method.Full code example
Full code example