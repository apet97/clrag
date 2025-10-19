# langsmith-trace-with-openai-agents-sdk

> Source: https://docs.langchain.com/langsmith/trace-with-openai-agents-sdk

The OpenAI Agents SDK allows you to build agentic applications powered by OpenAI’s models.
Learn how to trace your LLM applications using the OpenAI Agents SDK with LangSmith.
Installation
Requires Python SDK version langsmith>=0.3.15
.
Install LangSmith with OpenAI Agents support:
This will install both the LangSmith library and the OpenAI Agents SDK.
Quick Start
You can integrate LangSmith tracing with the OpenAI Agents SDK by using the OpenAIAgentsTracingProcessor
class.
The agent’s execution flow, including all spans and their details, will be logged to LangSmith.