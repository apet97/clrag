---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-local-server",
  "h1": "langsmith-local-server",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.460639",
  "sha256_raw": "96c2cc858caf6784e9773f3b03e3bd77f7428cd5ee80171851f2042a8f6c00f9"
}
---

# langsmith-local-server

> Source: https://docs.langchain.com/langsmith/local-server

langgraph new path/to/your/app --template new-langgraph-project-python
Additional templates
If you use langgraph new without specifying a template, you will be presented with an interactive menu that will allow you to choose from a list of available templates.
You will find a .env.example in the root of your new LangGraph app. Create a .env file in the root of your new LangGraph app and copy the contents of the .env.example file into it, filling in the necessary API keys:
from langgraph_sdk import get_clientimport asyncioclient = get_client(url="http://localhost:2024")async def main(): async for chunk in client.runs.stream( None, # Threadless run "agent", # Name of assistant. Defined in langgraph.json. input={ "messages": [{ "role": "human", "content": "What is LangGraph?", }], }, ): print(f"Receiving new event of type: {chunk.event}...") print(chunk.data) print("\n\n")asyncio.run(main())