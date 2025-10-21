---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-same-thread",
  "h1": "langsmith-same-thread",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.446575",
  "sha256_raw": "595f54b7702795406ce2103165bb4761a3423e6f0c58c3aa31c23967a078e22d"
}
---

# langsmith-same-thread

> Source: https://docs.langchain.com/langsmith/same-thread

In LangSmith Deployment, a thread is not explicitly associated with a particular agent.
This means that you can run multiple agents on the same thread, which allows a different agent to continue from an initial agent’s progress.In this example, we will create two agents and then call them both on the same thread.
You’ll see that the second agent will respond using information from the checkpoint generated in the thread by the first agent as context.
from langgraph_sdk import get_clientclient = get_client(url=<DEPLOYMENT_URL>)openai_assistant = await client.assistants.create( graph_id="agent", config={"configurable": {"model_name": "openai"}})# There should always be a default assistant with no configurationassistants = await client.assistants.search()default_assistant = [a for a in assistants if not a["config"]][0]
Now, we can run it on the default assistant and see that this second assistant is aware of the initial question, and can answer the question, “and you?”:
Python
Javascript
CURL
Copy
input = {"messages": [{"role": "user", "content": "and you?"}]}async for event in client.runs.stream( thread["thread_id"], default_assistant["assistant_id"], input=input, stream_mode="updates",): print(f"Receiving event of type: {event.event}") print(event.data) print("\n\n")
Output:
Copy
Receiving event of type: metadata{'run_id': '1ef6722d-80b3-6fbb-9324-253796b1cd13'}Receiving event of type: updates{'agent': {'messages': [{'content': [{'text': 'I am an artificial intelligence created by Anthropic, not by OpenAI. I should not have stated that OpenAI created me, as that is incorrect. Anthropic is the company that developed and trained me using advanced language models and AI technology. I will be more careful about providing accurate information regarding my origins in the future.', 'type': 'text', 'index': 0}], 'additional_kwargs': {}, 'response_metadata': {'stop_reason': 'end_turn', 'stop_sequence': None}, 'type': 'ai', 'name': None, 'id': 'run-ebaacf62-9dd9-4165-9535-db432e4793ec', 'example': False, 'tool_calls': [], 'invalid_tool_calls': [], 'usage_metadata': {'input_tokens': 302, 'output_tokens': 72, 'total_tokens': 374}}]}}