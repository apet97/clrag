---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-trace-with-langgraph",
  "h1": "langsmith-trace-with-langgraph",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.463922",
  "sha256_raw": "cec3b4b36c44cf6502b15fd9706edc72b4eeb2e627f634efe09ec76ca97813b5"
}
---

# langsmith-trace-with-langgraph

> Source: https://docs.langchain.com/langsmith/trace-with-langgraph

With LangChain
If you are using LangChain modules within LangGraph, you only need to set a few environment variables to enable tracing. This guide will walk through a basic example. For more detailed information on configuration, see the Trace With LangChain guide.1. Installation
Install the LangGraph library and the OpenAI integration for Python and JS (we use the OpenAI integration for the code snippets below). For a full list of packages available, see the LangChain Python docs and LangChain JS docs.2. Configure your environment
If you are using LangChain.js with LangSmith and are not in a serverless environment, we also recommend setting the following explicitly to reduce latency:
export LANGCHAIN_CALLBACKS_BACKGROUND=true
If you are in a serverless environment, we recommend setting the reverse to allow tracing to finish before your function ends:export LANGCHAIN_CALLBACKS_BACKGROUND=false
See this LangChain.js guide for more information.3. Log a trace
Once you’ve set up your environment, you can call LangChain runnables as normal. LangSmith will infer the proper tracing config:Without LangChain
If you are using other SDKs or custom functions within LangGraph, you will need to wrap or decorate them appropriately (with the@traceable
decorator in Python or the traceable
function in JS, or something like e.g. wrap_openai
for SDKs). If you do so, LangSmith will automatically nest traces from those wrapped methods.
Here’s an example. You can also see this page for more information.
1. Installation
Install the LangGraph library and the OpenAI SDK for Python and JS (we use the OpenAI integration for the code snippets below).2. Configure your environment
If you are using LangChain.js with LangSmith and are not in a serverless environment, we also recommend setting the following explicitly to reduce latency:
export LANGCHAIN_CALLBACKS_BACKGROUND=true
If you are in a serverless environment, we recommend setting the reverse to allow tracing to finish before your function ends:export LANGCHAIN_CALLBACKS_BACKGROUND=false
See this LangChain.js guide for more information.