---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-deployment-quickstart",
  "h1": "langsmith-deployment-quickstart",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.466787",
  "sha256_raw": "76b959a6196e9352a5cfb76db1cd2313582d49a7939577e87bed7badb4de8fda"
}
---

# langsmith-deployment-quickstart

> Source: https://docs.langchain.com/langsmith/deployment-quickstart

To deploy an application to LangSmith, your application code must reside in a GitHub repository. Both public and private repositories are supported. For this quickstart, use the new-langgraph-project template for your application:
Click the + New Deployment button. A pane will open where you can fill in the required fields.
If you are a first time user or adding a private repository that has not been previously connected, click the Import from GitHub button and follow the instructions to connect your GitHub account.
Select your New LangGraph Project repository.
Click Submit to deploy.
This may take about 15 minutes to complete. You can check the status in the Deployment details view.
from langgraph_sdk import get_clientclient = get_client(url="your-deployment-url", api_key="your-langsmith-api-key")async for chunk in client.runs.stream( None, # Threadless run "agent", # Name of assistant. Defined in langgraph.json. input={ "messages": [{ "role": "human", "content": "What is LangGraph?", }], }, stream_mode="updates",): print(f"Receiving new event of type: {chunk.event}...") print(chunk.data) print("\n\n")