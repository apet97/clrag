# langsmith-trace-without-env-vars

> Source: https://docs.langchain.com/langsmith/trace-without-env-vars

LANGSMITH_TRACING
LANGSMITH_API_KEY
LANGSMITH_ENDPOINT
LANGSMITH_PROJECT
Due to a number of asks for finer-grained control of tracing using the
trace
context manager, we changed the behavior of with trace
to honor the LANGSMITH_TRACING
environment variable in version 0.1.95 of the Python SDK. You can find more details in the release notes. The recommended way to disable/enable tracing without setting environment variables is to use the with tracing_context
context manager, as shown in the example below.- Python: The recommended way to do this in Python is to use the
tracing_context
context manager. This works for both code annotated withtraceable
and code within thetrace
context manager. - TypeScript: You can pass in both the client and the
tracingEnabled
flag to thetraceable
decorator.