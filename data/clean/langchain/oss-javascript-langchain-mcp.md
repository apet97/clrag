---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langchain-mcp",
  "h1": "oss-javascript-langchain-mcp",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.474573",
  "sha256_raw": "e4d02de3a82015ae4bbf3317407bf5ed0cbe444e3e190817b4838c447eb1327d"
}
---

# oss-javascript-langchain-mcp

> Source: https://docs.langchain.com/oss/javascript/langchain/mcp

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
langchain-mcp-adapters
library.
Install
Install the@langchain/mcp-adapters
library to use MCP tools in LangGraph:
Transport types
MCP supports different transport mechanisms for client-server communication:- stdio: Client launches server as a subprocess and communicates via standard input/output. Best for local tools and simple setups.
- Streamable HTTP: Server runs as an independent process handling HTTP requests. Supports remote connections and multiple clients.
- Server-Sent Events (SSE): a variant of streamable HTTP optimized for real-time streaming communication.
Use MCP tools
@langchain/mcp-adapters
enables agents to use tools defined across one or more MCP server.
Accessing multiple MCP servers
MultiServerMCPClient
is stateless by default. Each tool invocation creates a fresh MCP ClientSession
, executes the tool, and then cleans up.Custom MCP servers
To create your own MCP servers, you can use the@modelcontextprotocol/sdk
library. This library provides a simple way to define tools and run them as servers.
Math server (stdio transport)
Weather server (SSE transport)
Stateful tool usage
For stateful servers that maintain context between tool calls, useclient.session()
to create a persistent ClientSession
.
Using MCP ClientSession for stateful tool usage