---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-monorepo-support",
  "h1": "langsmith-monorepo-support",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.438995",
  "sha256_raw": "d00b28d0abdda0d8c93a05bfef43433e119ce23f2ae5ffeadaf55b3ebc6e7d91"
}
---

# langsmith-monorepo-support

> Source: https://docs.langchain.com/langsmith/monorepo-support

LangSmith supports deploying agents from monorepo setups where your agent code may depend on shared packages located elsewhere in the repository. This guide shows how to structure your monorepo and configure your langgraph.json file to work with shared dependencies.
Keep agent configs in agent directories: Place langgraph.json files in the specific agent directories, not at the monorepo root. This allows you to support multiple agents in the same monorepo, without having to deploy them all in the same LangGraph platform deployment.
Use relative paths for Python: For Python monorepos, use relative paths like "../../shared-package" in the dependencies array.
Leverage workspace features for JS: For JavaScript/TypeScript, use your package manager’s workspace features to manage dependencies between packages.
Test locally first: Always test your build locally before deploying to ensure all dependencies are correctly resolved.
Environment variables: Keep environment files (.env) in your agent directories for environment-specific configuration.