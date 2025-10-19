# langsmith-export-backend

> Source: https://docs.langchain.com/langsmith/export-backend

This section is only applicable for Kubernetes deployments.
- Collectors, such as OpenTelemetry, FluentBit or Prometheus.
- Observability backends, such as Datadog or the Grafana ecosystem.
Logs: OTel Example
All services that are part of the LangSmith self-hosted deployment write logs to their node’s filesystem and to stdout. In order to access these logs, you need to set up your collector to read from either the filesystem or stdout. Most popular collectors support reading logs from filesystems.- OpenTelemetry: File Log Receiver
- FluentBit: Tail Input
- Datadog: Kubernetes Log Collection
Metrics: OTel Example
LangSmith Services
The following LangSmith services expose metrics at an endpoint, in the Prometheus metrics format. The frontend does not currently expose metrics.- Backend:
http://<langsmith_release_name>-backend.<namespace>.svc.cluster.local:1984/metrics
- Platform Backend:
http://<langsmith_release_name>-platform-backend.<namespace>.svc.cluster.local:1986/metrics
- Playground:
http://<langsmith_release_name>-playground.<namespace>.svc.cluster.local:1988/metrics
- (LangSmith Control Plane only) Host Backend:
http://<langsmith_release_name>-host-backend.<namespace>.svc.cluster.local:1985/metrics
Frontend Nginx
The frontend service exposes its Nginx metrics at the following endpoint:langsmith-frontend.langsmith.svc.cluster.local:80/nginx_status
. You can either scrape them yourself, or bring up a Prometheus Nginx exporter using the LangSmith Observability Helm Chart
The following sections apply for in-cluster databases only. If you are using external databases, you will need to configure exposing and fetching metrics.
Postgres + Redis
If you are using in-cluster Postgres/Redis instances, you can use a Prometheus exporter to expose metrics from your instance. You can deploy your own, or if you would like, you can use the LangSmith Observability Helm Chart to deploy an exporter for you.Clickhouse
The in-cluster Clickhouse is configured to expose metrics without the need for an exporter. You can use your collector to scrape metrics athttp://<langsmith_release_name>-clickhouse.<namespace>.svc.cluster.local:9363/metrics
Traces: OTel Example
The LangSmith Backend, Platform Backend, Playground and LangSmith Queue deployments have been instrumented to emit Otel traces. Tracing is toggled off by default, and can be enabled for all LangSmith services with the following in yourlangsmith_config.yaml
(or equivalent) file: