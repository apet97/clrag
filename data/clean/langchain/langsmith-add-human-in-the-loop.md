---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-add-human-in-the-loop",
  "h1": "langsmith-add-human-in-the-loop",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.459044",
  "sha256_raw": "38f05cce06c83dee3444db2ac1390ff0ebcc80e956d8dc2a0e970194c189d158"
}
---

# langsmith-add-human-in-the-loop

> Source: https://docs.langchain.com/langsmith/add-human-in-the-loop

Dynamic interrupts
- Python
- JavaScript
- cURL
- The graph is invoked with some initial state.
- When the graph hits the interrupt, it returns an interrupt object with the payload and metadata.
3. The graph is resumed with a
Command(resume=...)
, injecting the human’s input and continuing execution.
Extended example: using `interrupt`
Extended example: using `interrupt`
This is an example graph you can run in the LangGraph API server.
See LangSmith quickstart for more details.
interrupt(...)
pauses execution athuman_node
, surfacing the given payload to a human.- Any JSON serializable value can be passed to the
interrupt
function. Here, a dict containing the text to revise. - Once resumed, the return value of
interrupt(...)
is the human-provided input, which is used to update the state.
- Python
- JavaScript
- cURL
- The graph is invoked with some initial state.
- When the graph hits the interrupt, it returns an interrupt object with the payload and metadata.
3. The graph is resumed with a
Command(resume=...)
, injecting the human’s input and continuing execution.
Static interrupts
Static interrupts (also known as static breakpoints) are triggered either before or after a node executes.Static interrupts are not recommended for human-in-the-loop workflows. They are best used for debugging and testing.
interrupt_before
and interrupt_after
at compile time:
- The breakpoints are set during
compile
time. interrupt_before
specifies the nodes where execution should pause before the node is executed.interrupt_after
specifies the nodes where execution should pause after the node is executed.
- Python
- JavaScript
- cURL
client.runs.wait
is called with theinterrupt_before
andinterrupt_after
parameters. This is a run-time configuration and can be changed for every invocation.interrupt_before
specifies the nodes where execution should pause before the node is executed.interrupt_after
specifies the nodes where execution should pause after the node is executed.
- Python
- JavaScript
- cURL
- The graph is run until the first breakpoint is hit.
- The graph is resumed by passing in
None
for the input. This will run the graph until the next breakpoint is hit.
Learn more
- Human-in-the-loop conceptual guide: learn more about LangGraph human-in-the-loop features.
- Common patterns: learn how to implement patterns like approving/rejecting actions, requesting user input, tool call review, and validating human input.