# langsmith-human-in-the-loop-time-travel

> Source: https://docs.langchain.com/langsmith/human-in-the-loop-time-travel

- Run the graph with initial inputs using LangGraph SDK’s client.runs.wait or client.runs.stream APIs.
- Identify a checkpoint in an existing thread: Use client.threads.get_history method to retrieve the execution history for a specific
thread_id
and locate the desiredcheckpoint_id
. Alternatively, set a breakpoint before the node(s) where you want execution to pause. You can then find the most recent checkpoint recorded up to that breakpoint. - (Optional) modify the graph state: Use the client.threads.update_state method to modify the graph’s state at the checkpoint and resume execution from alternative state.
- Resume execution from the checkpoint: Use the client.runs.wait or client.runs.stream APIs with an input of
None
and the appropriatethread_id
andcheckpoint_id
.
Use time travel in a workflow
Example graph
Example graph
1. Run the graph
- Python
- JavaScript
- cURL
2. Identify a checkpoint
- Python
- JavaScript
- cURL
3. Update the state
update_state
will create a new checkpoint. The new checkpoint will be associated with the same thread, but a new checkpoint ID.
- Python
- JavaScript
- cURL
4. Resume execution from the checkpoint
- Python
- JavaScript
- cURL
Learn more
- LangGraph time travel guide: learn more about using time travel in LangGraph.