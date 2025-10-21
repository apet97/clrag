---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langchain-ui",
  "h1": "oss-python-langchain-ui",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.482711",
  "sha256_raw": "6443b812c32996a6d492bc229c0cdddfa9a7a2b304d5d7f6bc65979bf774613a"
}
---

# oss-python-langchain-ui

> Source: https://docs.langchain.com/oss/python/langchain/ui

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
create_agent
. This UI is designed to provide rich, interactive experiences for your agents with minimal setup, whether you’re running locally or in a deployed context (such as LangSmith).
Agent Chat UI
Agent Chat UI is a Next.js application that provides a conversational interface for interacting with any LangChain agent. It supports real-time chat, tool visualization, and advanced features like time-travel debugging and state forking. Agent Chat UI is open source and can be adapted to your application needs.Features
Tool visualization
Tool visualization
Studio automatically renders tool calls and results in an intuitive interface.
Time-travel debugging
Time-travel debugging
Navigate through conversation history and fork from any point
State inspection
State inspection
View and modify agent state at any point during execution
Human-in-the-loop
Human-in-the-loop
Built-in support for reviewing and responding to agent requests
Quick start
The fastest way to get started is using the hosted version:- Visit Agent Chat UI
- Connect your agent by entering your deployment URL or local server address
- Start chatting - the UI will automatically detect and render tool calls and interrupts
Local development
For customization or local development, you can run Agent Chat UI locally:Connect to your agent
Agent Chat UI can connect to both local and deployed agents. After starting Agent Chat UI, you’ll need to configure it to connect to your agent:- Graph ID: Enter your graph name (find this under
graphs
in yourlanggraph.json
file) - Deployment URL: Your LangGraph server’s endpoint (e.g.,
http://localhost:2024
for local development, or your deployed agent’s URL) - LangSmith API key (optional): Add your LangSmith API key (not required if you’re using a local LangGraph server)