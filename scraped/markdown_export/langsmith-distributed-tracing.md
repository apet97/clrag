# langsmith-distributed-tracing

> Source: https://docs.langchain.com/langsmith/distributed-tracing

langsmith-trace
and optional baggage
for metadata/tags).
Example client-server setup:
- Trace starts on client
- Continues on server
Distributed tracing in Python
TracingMiddleware
.
The
TracingMiddleware
class was added in langsmith==0.1.133
.langsmith_extra
:
tracing_context
context manager. You can also directly specify the parent run context in the langsmith_extra
parameter of a method wrapped with @traceable
.
Distributed tracing in TypeScript
Distributed tracing in TypeScript requires
langsmith
version >=0.1.31
langsmith-trace
and baggage
header values, which we can pass to the server:
withRunTree
helper, which will ensure the run tree is propagated within traceable invocations.