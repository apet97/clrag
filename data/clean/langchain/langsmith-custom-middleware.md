---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-custom-middleware",
  "h1": "langsmith-custom-middleware",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.475253",
  "sha256_raw": "dd1685a36e2f4f53331f08cc58ee8548f73b506c0e29166067f44ed873ce5a47"
}
---

# langsmith-custom-middleware

> Source: https://docs.langchain.com/langsmith/custom-middleware

Starlette
app (including FastAPI
, FastHTML
and other compatible apps).
Adding middleware lets you intercept and modify requests and responses globally across your deployment, whether they’re hitting your custom endpoints or the built-in LangSmith APIs.
Below is an example using FastAPI.
“Python only”
We currently only support custom middleware in Python deployments with
langgraph-api>=0.0.26
.Create app
Starting from an existing LangSmith application, add the following middleware code to yourwebapp.py
file. If you are starting from scratch, you can create a new app from a template using the CLI.
Configure langgraph.json
Add the following to your langgraph.json
configuration file. Make sure the path points to the webapp.py
file you created above.
Customize middleware ordering
By default, custom middleware runs before authentication logic. To run custom middleware after authentication, setmiddleware_order
to auth_first
in your http
configuration. (This customization is supported starting with API server v0.4.35 and later.)
Start server
Test the server out locally:X-Custom-Header
in its response.