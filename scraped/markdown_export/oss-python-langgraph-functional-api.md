# oss-python-langgraph-functional-api

> Source: https://docs.langchain.com/oss/python/langgraph/functional-api

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
if
statements, for
loops, and function calls. Unlike many data orchestration frameworks that require restructuring code into an explicit pipeline or DAG, the Functional API allows you to incorporate these capabilities without enforcing a rigid execution model.
The Functional API uses two key building blocks:
@entrypoint
– Marks a function as the starting point of a workflow, encapsulating logic and managing execution flow, including handling long-running tasks and interrupts.@task
– Represents a discrete unit of work, such as an API call or data processing step, that can be executed asynchronously within an entrypoint. Tasks return a future-like object that can be awaited or resolved synchronously.
Functional API vs. Graph API
For users who prefer a more declarative approach, LangGraph’s Graph API allows you to define workflows using a Graph paradigm. Both APIs share the same underlying runtime, so you can use them together in the same application. Here are some key differences:- Control flow: The Functional API does not require thinking about graph structure. You can use standard Python constructs to define workflows. This will usually trim the amount of code you need to write.
- Short-term memory: The GraphAPI requires declaring a State and may require defining reducers to manage updates to the graph state.
@entrypoint
and@tasks
do not require explicit state management as their state is scoped to the function and is not shared across functions. - Checkpointing: Both APIs generate and use checkpoints. In the Graph API a new checkpoint is generated after every superstep. In the Functional API, when tasks are executed, their results are saved to an existing checkpoint associated with the given entrypoint instead of creating a new checkpoint.
- Visualization: The Graph API makes it easy to visualize the workflow as a graph which can be useful for debugging, understanding the workflow, and sharing with others. The Functional API does not support visualization as the graph is dynamically generated during runtime.
Example
Below we demonstrate a simple application that writes an essay and interrupts to request human review.Detailed Explanation
Detailed Explanation
This workflow will write an essay about the topic “cat” and then pause to get a review from a human. The workflow can be interrupted for an indefinite amount of time until a review is provided.When the workflow is resumed, it executes from the very start, but because the result of the An essay has been written and is ready for review. Once the review is provided, we can resume the workflow:The workflow has been completed and the review has been added to the essay.
writeEssay
task was already saved, the task result will be loaded from the checkpoint instead of being recomputed.Entrypoint
The@entrypoint
decorator can be used to create a workflow from a function. It encapsulates workflow logic and manages execution flow, including handling long-running tasks and interrupts.
Definition
An entrypoint is defined by decorating a function with the@entrypoint
decorator.
The function must accept a single positional argument, which serves as the workflow input. If you need to pass multiple pieces of data, use a dictionary as the input type for the first argument.
Decorating a function with an entrypoint
produces a Pregel
instance which helps to manage the execution of the workflow (e.g., handles streaming, resumption, and checkpointing).
You will usually want to pass a checkpointer to the @entrypoint
decorator to enable persistence and use features like human-in-the-loop.
- Sync
- Async
Injectable parameters
When declaring anentrypoint
, you can request access to additional parameters that will be injected automatically at run time. These parameters include:
| Parameter | Description |
|---|---|
| previous | Access the state associated with the previous checkpoint for the given thread. See short-term-memory. |
| store | An instance of [BaseStore][langgraph.store.base.BaseStore]. Useful for long-term memory. |
| writer | Use to access the StreamWriter when working with Async Python < 3.11. See streaming with functional API for details. |
| config | For accessing run time configuration. See RunnableConfig for information. |
Declare the parameters with the appropriate name and type annotation.
Requesting Injectable Parameters
Requesting Injectable Parameters
Executing
Using the@entrypoint
yields a Pregel
object that can be executed using the invoke
, ainvoke
, stream
, and astream
methods.
- Invoke
- Async Invoke
- Stream
- Async Stream
Resuming
Resuming an execution after an interrupt can be done by passing a resume value to the Command primitive.- Invoke
- Async Invoke
- Stream
- Async Stream
entrypoint
with a None
and the same thread id (config).
This assumes that the underlying error has been resolved and execution can proceed successfully.
- Invoke
- Async Invoke
- Stream
- Async Stream
Short-term memory
When anentrypoint
is defined with a checkpointer
, it stores information between successive invocations on the same thread id in checkpoints.
This allows accessing the state from the previous invocation using the previous
parameter.
By default, the previous
parameter is the return value of the previous invocation.
entrypoint.final
entrypoint.final
is a special primitive that can be returned from an entrypoint and allows decoupling the value that is saved in the checkpoint from the return value of the entrypoint.
The first value is the return value of the entrypoint, and the second value is the value that will be saved in the checkpoint. The type annotation is entrypoint.final[return_type, save_type]
.
Task
A task represents a discrete unit of work, such as an API call or data processing step. It has two key characteristics:- Asynchronous Execution: Tasks are designed to be executed asynchronously, allowing multiple operations to run concurrently without blocking.
- Checkpointing: Task results are saved to a checkpoint, enabling resumption of the workflow from the last saved state. (See persistence for more details).
Definition
Tasks are defined using the@task
decorator, which wraps a regular Python function.
Serialization
The outputs of tasks must be JSON-serializable to support checkpointing.
Execution
Tasks can only be called from within an entrypoint, another task, or a state graph node. Tasks cannot be called directly from the main application code. When you call a task, it returns immediately with a future object. A future is a placeholder for a result that will be available later. To obtain the result of a task, you can either wait for it synchronously (usingresult()
) or await it asynchronously (using await
).
- Synchronous Invocation
- Asynchronous Invocation
When to use a task
Tasks are useful in the following scenarios:- Checkpointing: When you need to save the result of a long-running operation to a checkpoint, so you don’t need to recompute it when resuming the workflow.
- Human-in-the-loop: If you’re building a workflow that requires human intervention, you MUST use tasks to encapsulate any randomness (e.g., API calls) to ensure that the workflow can be resumed correctly. See the determinism section for more details.
- Parallel Execution: For I/O-bound tasks, tasks enable parallel execution, allowing multiple operations to run concurrently without blocking (e.g., calling multiple APIs).
- Observability: Wrapping operations in tasks provides a way to track the progress of the workflow and monitor the execution of individual operations using LangSmith.
- Retryable Work: When work needs to be retried to handle failures or inconsistencies, tasks provide a way to encapsulate and manage the retry logic.
Serialization
There are two key aspects to serialization in LangGraph:entrypoint
inputs and outputs must be JSON-serializable.task
outputs must be JSON-serializable.
Determinism
To utilize features like human-in-the-loop, any randomness should be encapsulated inside of tasks. This guarantees that when execution is halted (e.g., for human in the loop) and then resumed, it will follow the same sequence of steps, even if task results are non-deterministic. LangGraph achieves this behavior by persisting task and subgraph results as they execute. A well-designed workflow ensures that resuming execution follows the same sequence of steps, allowing previously computed results to be retrieved correctly without having to re-execute them. This is particularly useful for long-running tasks or tasks with non-deterministic results, as it avoids repeating previously done work and allows resuming from essentially the same. While different runs of a workflow can produce different results, resuming a specific run should always follow the same sequence of recorded steps. This allows LangGraph to efficiently look up task and subgraph results that were executed prior to the graph being interrupted and avoid recomputing them.Idempotency
Idempotency ensures that running the same operation multiple times produces the same result. This helps prevent duplicate API calls and redundant processing if a step is rerun due to a failure. Always place API calls inside tasks functions for checkpointing, and design them to be idempotent in case of re-execution. Re-execution can occur if a task starts, but does not complete successfully. Then, if the workflow is resumed, the task will run again. Use idempotency keys or verify existing results to avoid duplication.Common Pitfalls
Handling side effects
Encapsulate side effects (e.g., writing to a file, sending an email) in tasks to ensure they are not executed multiple times when resuming a workflow.- Incorrect
- Correct
In this example, a side effect (writing to a file) is directly included in the workflow, so it will be executed a second time when resuming the workflow.
Non-deterministic control flow
Operations that might give different results each time (like getting current time or random numbers) should be encapsulated in tasks to ensure that on resume, the same result is returned.- In a task: Get random number (5) → interrupt → resume → (returns 5 again) → …
- Not in a task: Get random number (5) → interrupt → resume → get new random number (7) → …
interrupt
call may be matched with the wrong resume
value, leading to incorrect results.
Please read the section on determinism for more details.
- Incorrect
- Correct
In this example, the workflow uses the current time to determine which task to execute. This is non-deterministic because the result of the workflow depends on the time at which it is executed.