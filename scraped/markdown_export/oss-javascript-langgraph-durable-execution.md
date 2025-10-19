# oss-javascript-langgraph-durable-execution

> Source: https://docs.langchain.com/oss/javascript/langgraph/durable-execution

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
If you are using LangGraph with a checkpointer, you already have durable execution enabled. You can pause and resume workflows at any point, even after interruptions or failures.
To make the most of durable execution, ensure that your workflow is designed to be deterministic and idempotent and wrap any side effects or non-deterministic operations inside tasks. You can use tasks from both the StateGraph (Graph API) and the Functional API.
Requirements
To leverage durable execution in LangGraph, you need to:- Enable persistence in your workflow by specifying a checkpointer that will save workflow progress.
- Specify a thread identifier when executing a workflow. This will track the execution history for a particular instance of the workflow.
- Wrap any non-deterministic operations (e.g., random number generation) or operations with side effects (e.g., file writes, API calls) inside tasks to ensure that when a workflow is resumed, these operations are not repeated for the particular run, and instead their results are retrieved from the persistence layer. For more information, see Determinism and Consistent Replay.
Determinism and Consistent Replay
When you resume a workflow run, the code does NOT resume from the same line of code where execution stopped; instead, it will identify an appropriate starting point from which to pick up where it left off. This means that the workflow will replay all steps from the starting point until it reaches the point where it was stopped. As a result, when you are writing a workflow for durable execution, you must wrap any non-deterministic operations (e.g., random number generation) and any operations with side effects (e.g., file writes, API calls) inside tasks or nodes. To ensure that your workflow is deterministic and can be consistently replayed, follow these guidelines:- Avoid Repeating Work: If a node contains multiple operations with side effects (e.g., logging, file writes, or network calls), wrap each operation in a separate task. This ensures that when the workflow is resumed, the operations are not repeated, and their results are retrieved from the persistence layer.
- Encapsulate Non-Deterministic Operations: Wrap any code that might yield non-deterministic results (e.g., random number generation) inside tasks or nodes. This ensures that, upon resumption, the workflow follows the exact recorded sequence of steps with the same outcomes.
- Use Idempotent Operations: When possible ensure that side effects (e.g., API calls, file writes) are idempotent. This means that if an operation is retried after a failure in the workflow, it will have the same effect as the first time it was executed. This is particularly important for operations that result in data writes. In the event that a task starts but fails to complete successfully, the workflow’s resumption will re-run the task, relying on recorded outcomes to maintain consistency. Use idempotency keys or verify existing results to avoid unintended duplication, ensuring a smooth and predictable workflow execution.
Durability modes
LangGraph supports three durability modes that allow you to balance performance and data consistency based on your application’s requirements. The durability modes, from least to most durable, are as follows: A higher durability mode adds more overhead to the workflow execution.Added in v0.6.0
Use the
durability
parameter instead of checkpoint_during
(deprecated in v0.6.0) for persistence policy management:durability="async"
replacescheckpoint_during=True
durability="exit"
replacescheckpoint_during=False
checkpoint_during=True
->durability="async"
checkpoint_during=False
->durability="exit"
"exit"
Changes are persisted only when graph execution completes (either successfully or with an error). This provides the best performance for long-running graphs but means intermediate state is not saved, so you cannot recover from mid-execution failures or interrupt the graph execution.
"async"
Changes are persisted asynchronously while the next step executes. This provides good performance and durability, but there’s a small risk that checkpoints might not be written if the process crashes during execution.
"sync"
Changes are persisted synchronously before the next step starts. This ensures that every checkpoint is written before continuing execution, providing high durability at the cost of some performance overhead.
You can specify the durability mode when calling any graph execution method:
Using tasks in nodes
If a node contains multiple operations, you may find it easier to convert each operation into a task rather than refactor the operations into individual nodes.- Original
- With task
Resuming Workflows
Once you have enabled durable execution in your workflow, you can resume execution for the following scenarios:- Pausing and Resuming Workflows: Use the interrupt function to pause a workflow at specific points and the Command primitive to resume it with updated state. See Interrupts for more details.
- Recovering from Failures: Automatically resume workflows from the last successful checkpoint after an exception (e.g., LLM provider outage). This involves executing the workflow with the same thread identifier by providing it with a
null
as the input value (see this example with the functional API).
Starting Points for Resuming Workflows
- If you’re using a StateGraph (Graph API), the starting point is the beginning of the node where execution stopped.
- If you’re making a subgraph call inside a node, the starting point will be the parent node that called the subgraph that was halted. Inside the subgraph, the starting point will be the specific node where execution stopped.
- If you’re using the Functional API, the starting point is the beginning of the entrypoint where execution stopped.