---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-trace-with-vercel-ai-sdk",
  "h1": "langsmith-trace-with-vercel-ai-sdk",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.443555",
  "sha256_raw": "dde3a118edcbe6bc2cebd4c2fd791d22907613810d645788a9822fcf6d3a6e4c"
}
---

# langsmith-trace-with-vercel-ai-sdk

> Source: https://docs.langchain.com/langsmith/trace-with-vercel-ai-sdk

Installation
Install the Vercel AI SDK. This guide uses Vercel’s OpenAI integration for the code snippets below, but you can use any of their other options as well.
Environment configuration
Basic setup
Import and wrap AI SDK methods, then use them as you normally would:With traceable
You can wrap traceable
calls around AI SDK calls or within AI SDK tool calls. This is useful if you
want to group runs together in LangSmith:
Tracing in serverless environments
When tracing in serverless environments, you must wait for all runs to flush before your environment shuts down. To do this, you can pass a LangSmithClient
instance when wrapping the AI SDK method,
then call await client.awaitPendingTraceBatches()
.
Make sure to also pass it into any traceable
wrappers you create as well:
Next.js
, there is a convenient after
hook
where you can put this logic:
Passing LangSmith config
You can pass LangSmith-specific config to your wrapper both when initially wrapping your AI SDK methods and while running them viaproviderOptions.langsmith
.
This includes metadata (which you can later use to filter runs in LangSmith), top-level run name,
tags, custom client instances, and more.
Config passed while wrapping will apply to all future calls you make with the wrapped method:
providerOptions.langsmith
will apply only to that run.
We suggest importing and wrapping your config in createLangSmithProviderOptions
to ensure
proper typing:
Redacting data
You can customize what inputs and outputs the AI SDK sends to LangSmith by specifying custom input/output processing functions. This is useful if you are dealing with sensitive data that you would like to avoid sending to LangSmith. Because output formats vary depending on which AI SDK method you are using, we suggest defining and passing config individually into wrapped methods. You will also need to provide separate functions for child LLM runs within AI SDK calls, since callinggenerateText
at top level calls the LLM internally and can do so multiple times.
We also suggest passing a generic parameter into createLangSmithProviderOptions
to get proper types for inputs and outputs.
Here’s an example for generateText
:
execute
method in a traceable
like this:
traceable
return type is complex, which makes the cast necessary. You may also omit the AI SDK tool
wrapper function
if you wish to avoid the cast.