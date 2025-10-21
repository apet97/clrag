---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-self-host-using-an-existing-secret",
  "h1": "langsmith-self-host-using-an-existing-secret",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.433816",
  "sha256_raw": "74d0895bd5d12afd10492823c240d7c84f1d149b52f8efa01b08a63a2e40e57c"
}
---

# langsmith-self-host-using-an-existing-secret

> Source: https://docs.langchain.com/langsmith/self-host-using-an-existing-secret

langsmith-secrets
: This secret contains the license key and some other basic configuration parameters. You can see the template for this secret herelangsmith-redis
: This secret contains the Redis connection string and password. You can see the template for this secret herelangsmith-postgres
: This secret contains the Postgres connection string and password. You can see the template for this secret herelangsmith-clickhouse
: This secret contains the ClickHouse connection string and password. You can see the template for this secret here
Requirements
- An existing Kubernetes cluster
- A way to create Kubernetes secrets in your cluster. This can be done using
kubectl
, a Helm chart, or a secrets operator like Sealed Secrets
Parameters
You will need to create your own Kubernetes secrets that adhere to the structure of the secrets provisioned by the LangSmith Helm Chart.The secrets must have the same structure as the ones provisioned by the LangSmith Helm Chart (refer to the links above to see the specific secrets). If you miss any of the required keys, your LangSmith instance may not work correctly.
Configuration
With these secrets provisioned, you can configure your LangSmith instance to use the secrets directly to avoid passing in secret values through plaintext. You can do this by modifying thelangsmith_config.yaml
file for your LangSmith Helm Chart installation.