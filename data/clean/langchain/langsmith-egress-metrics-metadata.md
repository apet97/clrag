---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-egress-metrics-metadata",
  "h1": "langsmith-egress-metrics-metadata",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.475976",
  "sha256_raw": "eb6f35c1219d9b15312f57cefe5ff5566f46b022abb6b71f35a1d86856aae707"
}
---

# langsmith-egress-metrics-metadata

> Source: https://docs.langchain.com/langsmith/egress-metrics-metadata

Important: self-hosted only. This section only applies to customers who are not running in offline mode and assumes you are using a self-hosted LangSmith instance. This does not apply to cloud or hybrid deployments.
https://beacon.langchain.com
.
In the future, we will be introducing support diagnostics to help us ensure that LangSmith is running at an optimal level within your environment.
This will require egress to
https://beacon.langchain.com
from your network. If using an API key, you will also need to allow egress to https://api.smith.langchain.com
or https://eu.api.smith.langchain.com
for API key verification. Refer to the allowlisting IP section for static IP addresses, if needed.- Subscription Metrics
- Subscription metrics are used to determine level of access and utilization of LangSmith. This includes, but are not limited to:
- Nodes Executed
- Runs Executed
- License Key Verification
- Subscription metrics are used to determine level of access and utilization of LangSmith. This includes, but are not limited to:
- Operational Metadata
- This metadata will contain and collect the above subscription metrics to assist with remote support, allowing the LangChain team to diagnose and troubleshoot performance issues more effectively and proactively.
Example Payloads
In an effort to maximize transparency, we provide sample payloads here:License Verification (Enterprise)
Endpoint:POST beacon.langchain.com/v1/beacon/verify
Request:
API key verification (LangSmith API key)
Endpoint:POST api.smith.langchain.com/auth
Request:
Usage Reporting
Endpoint:POST beacon.langchain.com/v1/metadata/submit
Request: