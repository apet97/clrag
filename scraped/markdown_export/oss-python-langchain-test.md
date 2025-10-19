# oss-python-langchain-test

> Source: https://docs.langchain.com/oss/python/langchain/test

- Unit tests exercise small, deterministic pieces of your agent in isolation using in-memory fakes so you can assert exact behavior quickly and deterministically.
- Integration tests test the agent using real network calls to confirm that components work together, credentials and schemas line up, and latency is acceptable.
Unit Testing
Mocking Chat Model
For logic not requiring API calls, you can use an in-memory stub for mocking responses. LangChain providesGenericFakeChatModel
for mocking text responses. It accepts an iterator of responses (AIMessages or strings) and returns one per invocation. It supports both regular and streaming usage.
InMemorySaver Checkpointer
To enable persistence during testing, you can use theInMemorySaver
checkpointer. This allows you to simulate multiple turns to test state-dependent behavior:
Integration Testing
Many agent behaviors only emerge when using a real LLM, such as which tool the agent decides to call, how it formats responses, or whether a prompt modification affects the entire execution trajectory. LangChain’sagentevals
package provides evaluators specifically designed for testing agent trajectories with live models.
AgentEvals lets you easily evaluate the trajectory of your agent (the exact sequence of messages, including tool calls) by performing a trajectory match or by using an LLM judge:
Trajectory match
LLM-as-judge
Installing AgentEvals
Trajectory Match Evaluator
AgentEvals offers thecreate_trajectory_match_evaluator
function to match your agent’s trajectory against a reference trajectory. There are four modes to choose from:
| Mode | Description | Use Case |
|---|---|---|
strict | Exact match of messages and tool calls in the same order | Testing specific sequences (e.g., policy lookup before authorization) |
unordered | Same tool calls allowed in any order | Verifying information retrieval when order doesn’t matter |
subset | Agent calls only tools from reference (no extras) | Ensuring agent doesn’t exceed expected scope |
superset | Agent calls at least the reference tools (extras allowed) | Verifying minimum required actions are taken |
Strict match
Strict match
strict
mode ensures trajectories contain identical messages in the same order with the same tool calls, though it allows for differences in message content. This is useful when you need to enforce a specific sequence of operations, such as requiring a policy lookup before authorizing an action.Unordered match
Unordered match
unordered
mode allows the same tool calls in any order, which is helpful when you want to verify that specific information was retrieved but don’t care about the sequence. For example, an agent might need to check both weather and events for a city, but the order doesn’t matter.Subset and superset match
Subset and superset match
superset
and subset
modes match partial trajectories. The superset
mode verifies that the agent called at least the tools in the reference trajectory, allowing additional tool calls. The subset
mode ensures the agent did not call any tools beyond those in the reference.tool_args_match_mode
property and/or tool_args_match_overrides
to customize how the evaluator considers equality between tool calls in the actual trajectory vs. the reference. By default, only tool calls with the same arguments to the same tool are considered equal. Visit the repository for more details.LLM-as-Judge Evaluator
You can also use an LLM to evaluate the agent’s execution path with thecreate_trajectory_llm_as_judge
function. Unlike the trajectory match evaluators, it doesn’t require a reference trajectory, but one can be provided if available.
Without reference trajectory
Without reference trajectory
With reference trajectory
With reference trajectory
TRAJECTORY_ACCURACY_PROMPT_WITH_REFERENCE
prompt and configure the reference_outputs
variable:Async Support
Allagentevals
evaluators support Python asyncio. For evaluators that use factory functions, async versions are available by adding async
after create_
in the function name.
Async judge and evaluator example
Async judge and evaluator example
LangSmith Integration
For tracking experiments over time, you can log evaluator results to LangSmith, a platform for building production-grade LLM applications that includes tracing, evaluation, and experimentation tools. First, set up LangSmith by setting the required environment variables:evaluate
function.
Using pytest integration
Using pytest integration
Using the evaluate function
Using the evaluate function
evaluate
function:Recording & Replaying HTTP Calls
Integration tests that call real LLM APIs can be slow and expensive, especially when run frequently in CI/CD pipelines. We recommend using a library for recording HTTP requests and responses, then replaying them in subsequent runs without making actual network calls. You can usevcrpy
to achieve this. If you’re using pytest
, the pytest-recording
plugin provides a simple way to enable this with minimal configuration. Request/responses are recorded in cassettes, which are then used to mock the real network calls in subsequent runs.
Set up your conftest.py
file to filter out sensitive information from the cassettes:
vcr
marker:
--record-mode=once
option records HTTP interactions on the first run and replays them on subsequent runs.vcr
marker:
test_agent_trajectory.yaml
in the tests/cassettes
directory. Subsequent runs will use that cassette to mock the real network calls, granted the agent’s requests don’t change from the previous run. If they do, the test will fail and you’ll need to delete the cassette and rerun the test to record fresh interactions.