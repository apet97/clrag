---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-trace-with-openai-agents-sdk",
  "h1": "langsmith-trace-with-openai-agents-sdk",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.476744",
  "sha256_raw": "0fcf678f229b5b60da97c33edaf666e95ccac31ecf71c2572ce46ab7024bf2a0"
}
---

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