---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-use-tools",
  "h1": "langsmith-use-tools",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.484711",
  "sha256_raw": "2cf59866b42c7ac61fc9c0054f3ccac56fdf424bd5b2a8c9eefe2015df99cbf3"
}
---

# langsmith-use-tools

> Source: https://docs.langchain.com/langsmith/use-tools

Tools allow language models to interact with external systems and perform actions beyond just generating text. In the LangSmith playground, you can use two types of tools:
Built-in tools: Pre-configured tools provided by model providers (like OpenAI and Anthropic) that are ready to use. These include capabilities like web search, code interpretation, and more.
Custom tools: Functions you define to perform specific tasks. These are useful when you need to integrate with your own systems or create specialized functionality. When you define custom tools within the LangSmith Playground, you can verify that the model correctly identifies and calls these tools with the correct arguments. Soon we plan to support executing these custom tool calls directly.
The LangSmith Playground has native support for a variety of tools from OpenAI and Anthropic. If you want to use a tool that isn’t explicitly listed in the Playground, you can still add it by manually specifying its type and any required arguments.
In the tool section, select the built-in tool you want to use. You’ll only see the tools that are compatible with the provider and model you’ve chosen.
When the model calls the tool, the playground will display the response
Description: Clear explanation of what the tool does
Arguments: The inputs your tool requires
Note: When running a custom tool in the playground, the model will respond with a JSON object containing the tool name and the tool call. Currently, there’s no way to connect this to a hosted tool via MCP.
Some models provide control over which tools are called. To configure this:
Go to prompt settings
Navigate to tool settings
Select tool choice
To understand the available tool choice options, check the documentation for your specific provider. For example, OpenAI’s documentation on tool choice.