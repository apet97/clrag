---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-custom-routes",
  "h1": "langsmith-custom-routes",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.474044",
  "sha256_raw": "fb00c55c9918215e09b56b52c4639c751e77c3dfea027b5e682d9b52e2f72370"
}
---

# langsmith-custom-routes

> Source: https://docs.langchain.com/langsmith/custom-routes

Starlette
app (including FastAPI
, FastHTML
and other compatible apps). You make LangSmith aware of this by providing a path to the app in your langgraph.json
configuration file.
Defining a custom app object lets you add any routes you’d like, so you can do anything from adding a /login
endpoint to writing an entire full-stack web-app, all deployed in a single LangGraph Server.
Below is an example using FastAPI.
Create app
Starting from an existing LangSmith application, add the following custom route code to yourwebapp.py
file. If you are starting from scratch, you can create a new app from a template using the CLI.
Configure langgraph.json
Add the following to your langgraph.json
configuration file. Make sure the path points to the FastAPI application instance app
in the webapp.py
file you created above.
Start server
Test the server out locally:localhost:2024/hello
in your browser (2024
is the default development port), you should see the /hello
endpoint returning {"Hello": "World"}
.
Shadowing default endpoints
The routes you create in the app are given priority over the system defaults, meaning you can shadow and redefine the behavior of any default endpoint.