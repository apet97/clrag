---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-trace-with-semantic-kernel",
  "h1": "langsmith-trace-with-semantic-kernel",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.464545",
  "sha256_raw": "711ecf2c6db89688af62ab4e110d4bbe7542fad5db5d2c72d858d273b2ffc613"
}
---

# langsmith-trace-with-semantic-kernel

> Source: https://docs.langchain.com/langsmith/trace-with-semantic-kernel

Installation
Install the required packages using your preferred package manager:Requires LangSmith Python SDK version
langsmith>=0.4.26
for optimal OpenTelemetry support.Setup
1. Configure environment variables
Set your API keys and project name:2. Configure OpenTelemetry integration
In your Semantic Kernel application, import and configure the LangSmith OpenTelemetry integration along with the OpenAI instrumentor:You do not need to set any OpenTelemetry environment variables or configure exporters manually—
configure()
handles everything automatically.