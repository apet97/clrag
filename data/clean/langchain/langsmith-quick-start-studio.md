---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-quick-start-studio",
  "h1": "langsmith-quick-start-studio",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.435363",
  "sha256_raw": "0c5af5c6e90e7815925909f1347b231797c82b0cfeafec7d529ef097b0f1887f"
}
---

# langsmith-quick-start-studio

> Source: https://docs.langchain.com/langsmith/quick-start-studio

- Graphs deployed on cloud or self-hosted.
- Graphs running locally with LangGraph server.
Deployed graphs
Studio is accessed in the LangSmith UI from the Deployments navigation. For applications that are deployed, you can access Studio as part of that deployment. To do so, navigate to the deployment in the UI and select Studio. This will load Studio connected to your live deployment, allowing you to create, read, and update the threads, assistants, and memory in that deployment.Local development server
Prerequisites
To test your application locally using Studio:- Follow the local application quickstart first.
- If you don’t want data traced to LangSmith, set
LANGSMITH_TRACING=false
in your application’s.env
file. With tracing disabled, no data leaves your local server.
Setup
-
Install the LangGraph CLI:
This will start the LangGraph Server locally, running in-memory. The server will run in watch mode, listening for and automatically restarting on code changes. Read this reference to learn about all the options for starting the API server. You will see the following logs:Browser Compatibility Safari blocks
localhost
connections to Studio. To work around this, run the command with--tunnel
to access Studio via a secure tunnel.Once running, you will automatically be directed to Studio. -
For a running server, access the Dbugger with one of the following:
- Directly navigate to the following URL:
https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
. - Navigate to Deployments in the UI, click the Studio button on a deployment, enter
http://127.0.0.1:2024
and click Connect.
baseUrl
to match. - Directly navigate to the following URL:
(Optional) Attach a debugger
For step-by-step debugging with breakpoints and variable inspection, run the following:- VS Code
- PyCharm
Add this configuration to
launch.json
:Next steps
For more information on how to run Studio, refer to the following guides:- Run application
- Manage assistants
- Manage threads
- Iterate on prompts
- Debug LangSmith traces
- Add node to dataset