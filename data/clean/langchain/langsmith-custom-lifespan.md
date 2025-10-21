---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-custom-lifespan",
  "h1": "langsmith-custom-lifespan",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.434091",
  "sha256_raw": "18d1b97c6dec6b65c4f10d8f22947e10622ad60f22962b4d09596bac5b8f51ff"
}
---

# langsmith-custom-lifespan

> Source: https://docs.langchain.com/langsmith/custom-lifespan

When deploying agents to LangSmith, you often need to initialize resources like database connections when your server starts up, and ensure they’re properly closed when it shuts down. Lifespan events let you hook into your server’s startup and shutdown sequence to handle these critical setup and teardown tasks.
This works the same way as adding custom routes. You just need to provide your own Starlette
app (including FastAPI
, FastHTML
and other compatible apps).
Below is an example using FastAPI.
“Python only”
We currently only support custom lifespan events in Python deployments with langgraph-api>=0.0.26
.
Create app
Starting from an existing LangSmith application, add the following lifespan code to your webapp.py
file. If you are starting from scratch, you can create a new app from a template using the CLI.
Once you have a LangGraph project, add the following app code:
Add the following to your langgraph.json
configuration file. Make sure the path points to the webapp.py
file you created above.
Start server
Test the server out locally:
You should see your startup message printed when the server starts, and your cleanup message when you stop it with Ctrl+C
.
Deploying
You can deploy your app as-is to cloud or to your self-hosted platform.
Next steps
Now that you’ve added lifespan events to your deployment, you can use similar techniques to add custom routes or custom middleware to further customize your server’s behavior.