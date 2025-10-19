# langsmith-self-host-egress

> Source: https://docs.langchain.com/langsmith/self-host-egress

This section only applies to customers who are not running in offline mode and assumes you are using a self-hosted LangSmith instance serving version 0.9.0 or later. Previous versions of LangSmith did not have this feature.
https://beacon.langchain.com
.
In the future, we will be introducing support diagnostics to help us ensure that LangSmith is running at an optimal level within your environment.
Generally, data that we send to Beacon can be categorized as follows:
-
Subscription Metrics
-
Subscription metrics are used to determine level of access and utilization of LangSmith. This includes, but are not limited to:
- Number of traces
- Seats allocated per contract
- Seats in currently use
-
Subscription metrics are used to determine level of access and utilization of LangSmith. This includes, but are not limited to:
-
Operational Metadata
- This metadata will contain and collect the above subscription metrics to assist with remote support, allowing the LangChain team to diagnose and troubleshoot performance issues more effectively and proactively.
LangSmith Telemetry
As of version 0.11, LangSmith deployments will by default send telemetry data back to our backend. All telemetry data is associated with an organization and deployment, but never identified with individual users. We do not collect PII (personally identifiable information) in any form.What we use it for
- To provide more proactive support and faster troubleshooting of self-hosted instances.
- Assisting with performance tuning.
- Understanding real-world usage to prioritize improvements.
What we collect
- Request metadata: anonymized request counts, sizes, and durations.
- Database metrics: query durations, error rates, and performance counters.
- Distributed traces: end-to-end traces with timing and error information for high-latency or failed requests.
We do not collect actual payload contents, database records, or any data that can identify your end users or customers.
How to disable
Set the following values in yourlangsmith_config.yaml
file:
Example payloads
In an effort to maximize transparency, we provide sample payloads here:License Verification
Endpoint:POST beacon.langchain.com/v1/beacon/verify
Request:
Usage Reporting
Endpoint:POST beacon.langchain.com/v1/beacon/ingest-traces
Request:
Telemetry: Metrics
Endpoint:POST beacon.langchain.com/v1/beacon/v1/metrics
Request:
Telemetry: Traces
Endpoint:POST beacon.langchain.com/v1/beacon/v1/traces
Request: