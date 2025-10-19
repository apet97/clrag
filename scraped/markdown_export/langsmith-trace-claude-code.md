# langsmith-trace-claude-code

> Source: https://docs.langchain.com/langsmith/trace-claude-code

Quick Start
You can integrate LangSmith tracing with Claude Code by setting the following environment variables in the environment in which you run Claude Code.If you’re self-hosting LangSmith, replace the base endpoint with your LangSmith api endpoint and append
/api/v1
. For example: OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=https://ai-company.com/api/v1/otel/v1/claude_code