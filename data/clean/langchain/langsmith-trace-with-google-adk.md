---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-trace-with-google-adk",
  "h1": "langsmith-trace-with-google-adk",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.435033",
  "sha256_raw": "6158cab2a391a9fcb48bf1a1b7926aad1e37d3b3538c7e3a7d84d883b3c4098f"
}
---

# langsmith-trace-with-google-adk

> Source: https://docs.langchain.com/langsmith/trace-with-google-adk

Installation
Install the required packages using your preferred package manager:Requires LangSmith Python SDK version
langsmith>=0.4.26
for optimal OpenTelemetry support.Setup
1. Configure environment variables
Set your LangSmith API key and project name:2. Configure OpenTelemetry integration
In your Google ADK application, import and configure the LangSmith OpenTelemetry integration. This will automatically instrument Google ADK spans for OpenTelemetry.You do not need to set any OpenTelemetry environment variables or configure exporters manually—
configure()
handles everything automatically.3. Create and run your ADK agent
Once configured, your Google ADK application will automatically send traces to LangSmith: This example includes a minimal app that sets up an agent, session, and runner, then sends a message and streams events.View traces in LangSmith
- Agent conversations: Complete conversation flows between users and your ADK agents.
- Tool calls: Individual function calls made by your agents.
- Model interactions: LLM requests and responses using Gemini models.
- Session information: User and session context for organizing related traces.
- Model interactions: LLM requests and responses using Gemini models