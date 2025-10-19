# langsmith-sample-traces

> Source: https://docs.langchain.com/langsmith/sample-traces

Set a global sampling rate
This section is relevant for those using the LangSmith SDK or LangChain, not for those logging directly with the LangSmith API.
LANGSMITH_TRACING_SAMPLING_RATE
environment variable to any float between 0
(no traces) and 1
(all traces). For instance, setting the following environment variable will log 75% of the traces.
traceable
decorator and RunTree
objects.
Set different sampling rates per client
You can also set sampling rates on specificClient
instances and use the tracing_context
context manager: