---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-self-host-playground-environment-settings",
  "h1": "langsmith-self-host-playground-environment-settings",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.469957",
  "sha256_raw": "afa295d75a05deb7d0a882331d8243614610f736f2f29a3c4bf8d2615b4fae86"
}
---

# langsmith-self-host-playground-environment-settings

> Source: https://docs.langchain.com/langsmith/self-host-playground-environment-settings

This feature is only available on Helm chart versions 0.10.27 (application version 0.10.74) and later.
playground
service, which allows you to configure many of those environment variables directly on the pod itself. This can be useful to avoid having to set credentials in the UI.
Requirements
- A self-hosted LangSmith instance with the
playground
service running. - The provider you want to configure must support environment variables for configuration. Check the provider’s Chat Model documentation for more information.
- The secrets/roles you may want to attach to the
playground
service.- Note that for IRSA you may need to grant the
langsmith-playground
service account the necessary permissions to access the secrets or roles in your cloud provider.
- Note that for IRSA you may need to grant the
Configuration
With the parameters from above, you can configure your LangSmith instance to use environment variables for model providers. You can do this by modifying thelangsmith_config.yaml
file for your LangSmith Helm Chart installation or the docker-compose.yaml
file for your Docker installation.