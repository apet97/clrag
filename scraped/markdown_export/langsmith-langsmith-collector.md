# langsmith-langsmith-collector

> Source: https://docs.langchain.com/langsmith/langsmith-collector

This section is only applicable for Kubernetes deployments.
Receivers
Logs
This is an example for a Sidecar collector to read logs from its own pod, excluding logs from non domain-specific containers. A Sidecar configuration is useful here because we require access to every container’s filesystem. A DaemonSet can also be used.This configuration requires ‘get’, ‘list’, and ‘watch’ permissions on pods in the given namespace.
Metrics
Metrics can be scraped using the Prometheus endpoints. A single instance Gateway collector can be be used to avoid duplication of queries when fetching metrics. The following config scrapes all of the default named LangSmith services:This configuration requires ‘get’, ‘list’, and ‘watch’ permissions on pods, services and endpoints in the given namespace.
Traces
For traces, you need to enable the OTLP receiver. The following configuration can be used to listen to HTTP traces on port 4318, and GRPC on port 4317:Processors
Recommended OTEL Processors
The following processors are recommended when using the OTel collector:- Batch Processor: Groups the data into batches before sending to exporters.
- Memory Limiter: Prevents the collector from using too much memory and crashing. When the soft limit is crossed, the collector stops accepting new data.
- Kubernetes Attributes Processor: Adds Kubernetes metadata such as pod name into the telemetry data.