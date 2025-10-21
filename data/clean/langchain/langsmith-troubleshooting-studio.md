---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-troubleshooting-studio",
  "h1": "langsmith-troubleshooting-studio",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.462649",
  "sha256_raw": "70d41cdec02bcf1794596784e1fbb73d982d1861788280fb584b8afbea3af4ea"
}
---

# langsmith-troubleshooting-studio

> Source: https://docs.langchain.com/langsmith/troubleshooting-studio

Brave blocks plain-HTTP traffic on localhost when Brave Shields are enabled. When running Studio with langgraph dev, you may see “Failed to load assistants” errors.
Undefined conditional edges may show unexpected connections in your graph. This is
because without proper definition, Studio assumes the conditional edge could access all other nodes. To address this, explicitly define the routing paths using one of these methods:
Deployed application: If your application is deployed on LangSmith, you may need to create a new revision to enable this feature.
Local development server: If you are running your application locally, make sure you have upgraded to the latest version of the langgraph-cli (pip install -U langgraph-cli). Additionally, ensure you have tracing enabled by setting the LANGSMITH_API_KEY in your project’s .env file.
When you run an experiment, any attached evaluators are scheduled for execution in a queue. If you don’t see results immediately, it likely means they are still pending.