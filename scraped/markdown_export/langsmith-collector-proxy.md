# langsmith-collector-proxy

> Source: https://docs.langchain.com/langsmith/collector-proxy

This is a beta feature. The API may change in future releases.
When to Use the Collector-Proxy
The Collector-Proxy is particularly valuable when:- You’re running multiple instances of your application in parallel and need to efficiently aggregate traces
- You want more efficient tracing than direct OTEL API calls to LangSmith (the collector optimizes batching and compression)
- You’re using a language that doesn’t have a native LangSmith SDK
Key Features
- Efficient Data Transfer Batches multiple spans into fewer, larger uploads.
- Compression Uses zstd to minimize payload size.
- OTLP Support Accepts OTLP JSON and Protobuf over HTTP POST.
- Semantic Translation Maps GenAI/OpenInference conventions to the LangSmith Run model.
- Flexible Batching Flush by span count or time interval.
Configuration
Configure via environment variables:| Variable | Description | Default |
|---|---|---|
HTTP_PORT | Port to run the proxy server | 4318 |
LANGSMITH_ENDPOINT | LangSmith backend URL | https://api.smith.langchain.com |
LANGSMITH_API_KEY | API key for LangSmith | Required (env var or header) |
LANGSMITH_PROJECT | Default tracing project | Default project if not specified |
BATCH_SIZE | Spans per upload batch | 100 |
FLUSH_INTERVAL_MS | Flush interval in milliseconds | 1000 |
MAX_BUFFER_BYTES | Max uncompressed buffer size | 10485760 (10 MB) |
MAX_BODY_BYTES | Max incoming request body size | 209715200 (200 MB) |
MAX_RETRIES | Retry attempts for failed uploads | 3 |
RETRY_BACKOFF_MS | Initial backoff in milliseconds | 100 |
Project Configuration
The Collector-Proxy supports LangSmith project configuration with the following priority:- If a project is specified in the request headers (
Langsmith-Project
), that project will be used - If no project is specified in headers, it will use the project set in the
LANGSMITH_PROJECT
environment variable - If neither is set, it will trace to the
default
project.
Authentication
The API key can be provided either:- As an environment variable (
LANGSMITH_API_KEY
) - In the request headers (
X-API-Key
)
Deployment (Docker)
You can deploy the Collector-Proxy with Docker:-
Build the image
-
Run the container
Usage
Point any OTLP-compatible client or the OpenTelemetry Collector exporter at:Health & Scaling
- Liveness:
GET /live
→ 200 - Readiness:
GET /ready
→ 200
Horizontal Scaling
To ensure full traces are batched correctly, route spans with the same trace ID to the same instance (e.g., via consistent hashing).Fork & Extend
Fork the Collector-Proxy repo on GitHub and implement your own converter:- Create a custom
GenAiConverter
or modify the existing one ininternal/translator/otel_converter.go
- Register the custom converter in
internal/translator/translator.go