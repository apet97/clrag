---
{
  "url": "",
  "namespace": "langchain",
  "title": "oss-javascript-langgraph-local-server",
  "h1": "oss-javascript-langgraph-local-server",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.455106",
  "sha256_raw": "f631c959373fc9816aa60341983a322299b780c882dad19b23f58c3298c36097"
}
---

# oss-javascript-langgraph-local-server

> Source: https://docs.langchain.com/oss/javascript/langgraph/local-server

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Prerequisites
Before you begin, ensure you have the following:- An API key for LangSmith - free to sign up
1. Install the LangGraph CLI
2. Create a LangGraph app 🌱
Create a new app from thenew-langgraph-project-js
template. This template demonstrates a single-node application you can extend with your own logic.
3. Install dependencies
In the root of your new LangGraph app, install the dependencies inedit
mode so your local changes are used by the server:
4. Create a .env
file
You will find a .env.example
in the root of your new LangGraph app. Create a .env
file in the root of your new LangGraph app and copy the contents of the .env.example
file into it, filling in the necessary API keys:
5. Launch LangGraph Server 🚀
Start the LangGraph API server locally:langgraph dev
command starts LangGraph Server in an in-memory mode. This mode is suitable for development and testing purposes. For production use, deploy LangGraph Server with access to a persistent storage backend. For more information, see the Hosting overview.
6. Test your application in Studio
Studio is a specialized UI that you can connect to LangGraph API server to visualize, interact with, and debug your application locally. Test your graph in Studio by visiting the URL provided in the output of thelanggraph dev
command:
Safari compatibility
Safari compatibility
Use the
--tunnel
flag with your command to create a secure tunnel, as Safari has limitations when connecting to localhost servers:7. Test the API
- Javascript SDK
- Rest API
- Install the LangGraph JS SDK:
- Send a message to the assistant (threadless run):
Next steps
Now that you have a LangGraph app running locally, take your journey further by exploring deployment and advanced features:- Deployment quickstart: Deploy your LangGraph app using LangSmith.
- LangSmith: Learn about foundational LangSmith concepts.
- JS/TS SDK Reference: Explore the JS/TS SDK API Reference.