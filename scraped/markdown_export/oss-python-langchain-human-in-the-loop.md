# oss-python-langchain-human-in-the-loop

> Source: https://docs.langchain.com/oss/python/langchain/human-in-the-loop

LangChain v1.0Welcome to the new LangChain documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
approve
), modified before running (edit
), or rejected with feedback (reject
).
Interrupt decision types
The middleware defines three built-in ways a human can respond to an interrupt:| Decision Type | Description | Example Use Case |
|---|---|---|
✅ approve | The action is approved as-is and executed without changes. | Send an email draft exactly as written |
✏️ edit | The tool call is executed with modifications. | Change the recipient before sending an email |
❌ reject | The tool call is rejected, with an explanation added to the conversation. | Reject an email draft and explain how to rewrite it |
interrupt_on
.
When multiple tool calls are paused at the same time, each action requires a separate decision.
Decisions must be provided in the same order as the actions appear in the interrupt request.
When editing tool arguments, make changes conservatively. Significant modifications to the original arguments may cause the model to re-evaluate its approach and potentially execute the tool multiple times or take unexpected actions.
Configuring interrupts
To use HITL, add the middleware to the agent’smiddleware
list when creating the agent.
You configure it with a mapping of tool actions to the decision types that are allowed for each action. The middleware will interrupt execution when a tool call matches an action in the mapping.
You must configure a checkpointer to persist the graph state across interrupts.
In production, use a persistent checkpointer like
AsyncPostgresSaver
. For testing or prototyping, use InMemorySaver
.When invoking the agent, pass a config
that includes the thread ID to associate execution with a conversation thread.
See the LangGraph interrupts documentation for details.Responding to interrupts
When you invoke the agent, it runs until it either completes or an interrupt is raised. An interrupt is triggered when a tool call matches the policy you configured ininterrupt_on
. In that case, the invocation result will include an __interrupt__
field with the actions that require review. You can then present those actions to a reviewer and resume execution once decisions are provided.
Decision types
- ✅ approve
- ✏️ edit
- ❌ reject
Use
approve
to approve the tool call as-is and execute it without changes.Execution lifecycle
The middleware defines anafter_model
hook that runs after the model generates a response but before any tool calls are executed:
- The agent invokes the model to generate a response.
- The middleware inspects the response for tool calls.
- If any calls require human input, the middleware builds a
HITLRequest
withaction_requests
andreview_configs
and calls interrupt. - The agent waits for human decisions.
- Based on the
HITLResponse
decisions, the middleware executes approved or edited calls, synthesizes ToolMessage’s for rejected calls, and resumes execution.