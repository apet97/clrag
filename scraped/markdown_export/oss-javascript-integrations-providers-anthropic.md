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