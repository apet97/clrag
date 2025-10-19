# langsmith-serverless-environments

> Source: https://docs.langchain.com/langsmith/serverless-environments

When tracing JavaScript functions, LangSmith will trace runs in the background by default to avoid adding latency. In serverless environments where the execution context may be terminated abruptly, it’s important to ensure that all tracing data is properly flushed before the function completes.
To make sure this occurs, you can either:
- Set an environment variable named
LANGSMITH_TRACING_BACKGROUND
to"false"
. This will cause your traced functions to wait for tracing to complete before returning.- Note that this is named differently from the environment variable in LangChain.js because LangSmith can be used without LangChain.
- Pass a custom client into your traced runs and
await
theclient.awaitPendingTraceBatches();
method.
awaitPendingTraceBatches
alongside the traceable
method:
manualFlushMode: true
in your client like this:
client.flush()
like this before your serverless function closes:
.flush()
.