---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-trace-with-autogen",
  "h1": "langsmith-trace-with-autogen",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.460146",
  "sha256_raw": "0b09ff678194adc9f9a801360d1881bb058a0b1f79233251cc6adfc0438ffa19"
}
---

# langsmith-trace-with-autogen

> Source: https://docs.langchain.com/langsmith/trace-with-autogen

Installation
Install the required packages using your preferred package manager:Requires LangSmith Python SDK version
langsmith>=0.4.26
for optimal OpenTelemetry support.Setup
1. Configure environment variables
Set your API keys and project name:2. Configure OpenTelemetry integration
In your AutoGen application, import and configure the LangSmith OpenTelemetry integration along with the AutoGen and OpenAI instrumentors:You do not need to set any OpenTelemetry environment variables or configure exporters manually—
configure()
handles everything automatically.