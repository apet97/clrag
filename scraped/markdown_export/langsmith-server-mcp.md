# langsmith-server-mcp

> Source: https://docs.langchain.com/langsmith/server-mcp

/mcp
on LangGraph Server.
You can set up custom authentication middleware to authenticate a user with an MCP server to get access to user-scoped tools within your LangSmith deployment.
An example architecture for this flow:
Requirements
To use MCP, ensure you have the following dependencies installed:langgraph-api >= 0.2.3
langgraph-sdk >= 0.1.61
Usage overview
To enable MCP:- Upgrade to use langgraph-api>=0.2.3. If you are deploying LangSmith, this will be done for you automatically if you create a new revision.
- MCP tools (agents) will be automatically exposed.
- Connect with any MCP-compliant client that supports Streamable HTTP.
Client
Use an MCP-compliant client to connect to the LangGraph server. The following examples show how to connect using different programming languages.- JavaScript/TypeScript
- Python
Note
Replace serverUrl
with your LangGraph server URL and configure authentication headers as needed.
Expose an agent as MCP tool
When deployed, your agent will appear as a tool in the MCP endpoint with this configuration:- Tool name: The agent’s name.
- Tool description: The agent’s description.
- Tool input schema: The agent’s input schema.
Setting name and description
You can set the name and description of your agent inlanggraph.json
:
Schema
Define clear, minimal input and output schemas to avoid exposing unnecessary internal complexity to the LLM. The default MessagesState usesAnyMessage
, which supports many message types but is too general for direct LLM exposure.
Instead, define custom agents or workflows that use explicitly typed input and output structures.
For example, a workflow answering documentation questions might look like this:
Use user-scoped MCP tools in your deployment
To make user-scoped tools available to your LangSmith deployment, start with implementing a snippet like the following:
- MCP only supports adding headers to requests made to
streamable_http
andsse
transport
servers. - Your MCP server URL.
- Get available tools from your MCP server.
Session behavior
The current LangGraph MCP implementation does not support sessions. Each/mcp
request is stateless and independent.
Authentication
The/mcp
endpoint uses the same authentication as the rest of the LangGraph API. Refer to the authentication guide for setup details.
Disable MCP
To disable the MCP endpoint, setdisable_mcp
to true
in your langgraph.json
configuration file:
/mcp
endpoint.