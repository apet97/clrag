# langsmith-stateless-runs

> Source: https://docs.langchain.com/langsmith/stateless-runs

Most of the time, you provide a thread_id to your client when you run your graph in order to keep track of prior runs through the persistent state implemented in LangSmith Deployment. However, if you don’t need to persist the runs you don’t need to use the built-in persistent state and can create stateless runs.
from langgraph_sdk import get_clientclient = get_client(url=<DEPLOYMENT_URL>)# Using the graph deployed with the name "agent"assistant_id = "agent"# create threadthread = await client.threads.create()
We can stream the results of a stateless run in an almost identical fashion to how we stream from a run with the state attribute, but instead of passing a value to the thread_id parameter, we pass None:
Python
Javascript
CURL
Copy
input = { "messages": [ {"role": "user", "content": "Hello! My name is Bagatur and I am 26 years old."} ]}async for chunk in client.runs.stream( # Don't pass in a thread_id and the stream will be stateless None, assistant_id, input=input, stream_mode="updates",): if chunk.data and "run_id" not in chunk.data: print(chunk.data)
Output:
Copy
{'agent': {'messages': [{'content': "Hello Bagatur! It's nice to meet you. Thank you for introducing yourself and sharing your age. Is there anything specific you'd like to know or discuss? I'm here to help with any questions or topics you're interested in.", 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'ai', 'name': None, 'id': 'run-489ec573-1645-4ce2-a3b8-91b391d50a71', 'example': False, 'tool_calls': [], 'invalid_tool_calls': [], 'usage_metadata': None}]}}
{'messages': [{'content': 'Hello! My name is Bagatur and I am 26 years old.','additional_kwargs': {},'response_metadata': {},'type': 'human','name': None,'id': '5e088543-62c2-43de-9d95-6086ad7f8b48','example': False},{'content': "Hello Bagatur! It's nice to meet you. Thank you for introducing yourself and sharing your age. Is there anything specific you'd like to know or discuss? I'm here to help with any questions or topics you'd like to explore.",'additional_kwargs': {},'response_metadata': {},'type': 'ai','name': None,'id': 'run-d6361e8d-4d4c-45bd-ba47-39520257f773','example': False,'tool_calls': [],'invalid_tool_calls': [],'usage_metadata': None}]}