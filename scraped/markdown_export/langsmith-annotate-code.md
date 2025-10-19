# langsmith-annotate-code

> Source: https://docs.langchain.com/langsmith/annotate-code

If you’ve decided you no longer want to trace your runs, you can remove the
LANGSMITH_TRACING
environment variable. Note that this does not affect the RunTree
objects or API users, as these are meant to be low-level and not affected by the tracing toggle.Use @traceable
/ traceable
LangSmith makes it easy to log traces with minimal changes to your existing code with the @traceable
decorator in Python and traceable
function in TypeScript.
The
LANGSMITH_TRACING
environment variable must be set to 'true'
in order for traces to be logged to LangSmith, even when using @traceable
or traceable
. This allows you to toggle tracing on and off without changing your code.Additionally, you will need to set the LANGSMITH_API_KEY
environment variable to your API key (see Setup for more information).By default, the traces will be logged to a project named default
. To log traces to a different project, see this section.@traceable
decorator is a simple way to log traces from the LangSmith Python SDK. Simply decorate any function with @traceable
.
Note that when wrapping a sync function with traceable
, (e.g. formatPrompt
in the example below), you should use the await
keyword when calling it to
ensure the trace is logged correctly.
Use the trace
context manager (Python only)
In Python, you can use the trace
context manager to log traces to LangSmith. This is useful in situations where:
- You want to log traces for a specific block of code.
- You want control over the inputs, outputs, and other attributes of the trace.
- It is not feasible to use a decorator or wrapper.
- Any or all of the above.
traceable
decorator and wrap_openai
wrapper, so you can use them together in the same application.
Use the RunTree
API
Another, more explicit way to log traces to LangSmith is via the RunTree
API. This API allows you more control over your tracing - you can manually create runs and children runs to assemble your trace. You still need to set your LANGSMITH_API_KEY
, but LANGSMITH_TRACING
is not necessary for this method.
This method is not recommended, as it’s easier to make mistakes in propagating trace context.
Example usage
You can extend the utilities above to conveniently trace any code. Below are some example extensions: Trace any public method in a class:Ensure all traces are submitted before exiting
LangSmith’s tracing is done in a background thread to avoid obstructing your production application. This means that your process may end before all traces are successfully posted to LangSmith. Here are some options for ensuring all traces are submitted before exiting your application.Using the LangSmith SDK
If you are using the LangSmith SDK standalone, you can use theflush
method before exit: