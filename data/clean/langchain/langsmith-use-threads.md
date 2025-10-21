---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-use-threads",
  "h1": "langsmith-use-threads",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.488893",
  "sha256_raw": "d7bd07d87356f3e9fcb68f0f5f0afe050634736b52f0bab9eecd636c14bd41dc"
}
---

# langsmith-use-threads

> Source: https://docs.langchain.com/langsmith/use-threads

Alternatively, if you already have a thread in your application whose state you wish to copy, you can use the copy method. This will create an independent thread whose history is identical to the original thread at the time of the operation. See the Python and JS SDK reference docs for more information.
Finally, you can create a thread with an arbitrary pre-defined state by providing a list of supersteps into the create method. The supersteps describe a list of a sequence of state updates. For example:
To list threads, use the LangGraph SDKsearch method. This will list the threads in the application that match the provided filters. See the Python and JS SDK reference docs for more information.
Use the status field to filter threads based on their status. Supported values are idle, busy, interrupted, and error. See here for information on each status. For example, to view idle threads:
You can also view threads in a deployment via the LangSmith UI.Inside your deployment, select the “Threads” tab. This will load a table of all of the threads in your deployment.To filter by thread status, select a status in the top bar. To sort by a supported property, click on the arrow icon for the desired column.
To view a thread’s history, use the get_history method. This returns a list of every state the thread experienced. For more information see the Python and JS reference docs.
You can also view threads in a deployment via the LangSmith UI.Inside your deployment, select the “Threads” tab. This will load a table of all of the threads in your deployment.Select a thread to inspect its current state. To view its full history and for further debugging, open the thread in Studio.