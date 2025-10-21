---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-python-langgraph-use-functional-api",
  "h1": "oss-python-langgraph-use-functional-api",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.479402",
  "sha256_raw": "607f08ed3b03ef41125e66e58b4bc943a95efa8d64f2b7d85ea9470e4438a3c2"
}
---

# oss-python-langgraph-use-functional-api

> Source: https://docs.langchain.com/oss/python/langgraph/use-functional-api

Creating a simple workflow
When defining anentrypoint
, input is restricted to the first argument of the function. To pass multiple inputs, you can use a dictionary.
Extended example: simple workflow
Extended example: simple workflow
Extended example: Compose an essay with an LLM
Extended example: Compose an essay with an LLM
@task
and @entrypoint
decorators
syntactically. Given that a checkpointer is provided, the workflow results will
be persisted in the checkpointer.Parallel execution
Tasks can be executed in parallel by invoking them concurrently and waiting for the results. This is useful for improving performance in IO bound tasks (e.g., calling APIs for LLMs).Extended example: parallel LLM calls
Extended example: parallel LLM calls
@task
. Each call generates a paragraph on a different topic, and results are joined into a single text output.Calling graphs
The Functional API and the Graph API can be used together in the same application as they share the same underlying runtime.Extended example: calling a simple graph from the functional API
Extended example: calling a simple graph from the functional API
Call other entrypoints
You can call other entrypoints from within an entrypoint or a task.Extended example: calling another entrypoint
Extended example: calling another entrypoint
Streaming
The Functional API uses the same streaming mechanism as the Graph API. Please read the streaming guide section for more details. Example of using the streaming API to stream both updates and custom data.- Import
get_stream_writer
fromlanggraph.config
. - Obtain a stream writer instance within the entrypoint.
- Emit custom data before computation begins.
- Emit another custom message after computing the result.
- Use
.stream()
to process streamed output. - Specify which streaming modes to use.
get_stream_writer
will not work. Instead please
use the StreamWriter
class directly. See Async with Python < 3.11 for more details.Retry policy
Caching Tasks
ttl
is specified in seconds. The cache will be invalidated after this time.
Resuming after an error
slow_task
as its result is already saved in the checkpoint.
Human-in-the-loop
The functional API supports human-in-the-loop workflows using theinterrupt
function and the Command
primitive.
Basic human-in-the-loop workflow
We will create three tasks:- Append
"bar"
. - Pause for human input. When resuming, append human input.
- Append
"qux"
.
step_1
— are persisted, so that they are not run again following the interrupt
.
Let’s send in a query string:
interrupt
after step_1
. The interrupt provides instructions to resume the run. To resume, we issue a Command containing the data expected by the human_feedback
task.
Review tool calls
To review tool calls before execution, we add areview_tool_call
function that calls interrupt
. When this function is called, execution will be paused until we issue a command to resume it.
Given a tool call, our function will interrupt
for human review. At that point we can either:
- Accept the tool call
- Revise the tool call and continue
- Generate a custom tool message (e.g., instructing the model to re-format its tool call)
ToolMessage
supplied by the human. The results of prior tasks — in this case the initial model call — are persisted, so that they are not run again following the interrupt
.
Short-term memory
Short-term memory allows storing information across different invocations of the same thread id. See short-term memory for more details.Manage checkpoints
You can view and delete the information stored by the checkpointer.View thread state
View the history of the thread
Decouple return value from saved value
Useentrypoint.final
to decouple what is returned to the caller from what is persisted in the checkpoint. This is useful when:
- You want to return a computed result (e.g., a summary or status), but save a different internal value for use on the next invocation.
- You need to control what gets passed to the previous parameter on the next run.
Chatbot example
An example of a simple chatbot using the functional API and theInMemorySaver
checkpointer.
The bot is able to remember the previous conversation and continue from where it left off.
Long-term memory
long-term memory allows storing information across different thread ids. This could be useful for learning information about a given user in one conversation and using it in another.Workflows
- Workflows and agent guide for more examples of how to build workflows using the Functional API.
Integrate with other libraries
- Add LangGraph’s features to other frameworks using the functional API: Add LangGraph features like persistence, memory and streaming to other agent frameworks that do not provide them out of the box.