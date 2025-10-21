---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-integrations-providers-anthropic",
  "h1": "oss-javascript-integrations-providers-anthropic",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.490678",
  "sha256_raw": "5e3c66d6007d364f6bb60f0727e04348d3f5a1f99327d9602cd550dc89395b03"
}
---

# oss-javascript-integrations-providers-anthropic

> Source: https://docs.langchain.com/oss/javascript/integrations/providers/anthropic

Prompting Best Practices
Anthropic models have several prompting best practices compared to OpenAI models. System Messages may only be the first message Anthropic models require any system messages to be the first one in your prompts.ChatAnthropic
ChatAnthropic
is a subclass of LangChain’s ChatModel
, meaning it works best with ChatPromptTemplate
.
You can import this wrapper with the following code:
npm
ChatPromptTemplate
s.
Here is an example below of doing that: