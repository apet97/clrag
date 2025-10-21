---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-trace-openai",
  "h1": "langsmith-trace-openai",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.459270",
  "sha256_raw": "3cf65d8f2f4e790ba69b01ce33266a555d460995c3a42ab52f4b4ce52d22270e"
}
---

# langsmith-trace-openai

> Source: https://docs.langchain.com/langsmith/trace-openai

wrap_openai
/wrapOpenAI
methods in Python/TypeScript allow you to wrap your OpenAI client in order to automatically log traces — no decorator or function wrapping required! Using the wrapper ensures that messages, including tool calls and multimodal content blocks will be rendered nicely in LangSmith. Also note that the wrapper works seamlessly with the @traceable
decorator or traceable
function and you can use both in the same application.
The
LANGSMITH_TRACING
environment variable must be set to 'true'
in order for traces to be logged to LangSmith, even when using wrap_openai
or wrapOpenAI
. This allows you to toggle tracing on and off without changing your code.Additionally, you will need to set the LANGSMITH_API_KEY
environment variable to your API key (see Setup for more information).If your LangSmith API key is linked to multiple workspaces, set the LANGSMITH_WORKSPACE_ID
environment variable to specify which workspace to use.By default, the traces will be logged to a project named default
. To log traces to a different project, see this section.