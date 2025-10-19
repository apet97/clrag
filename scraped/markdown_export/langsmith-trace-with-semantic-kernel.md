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