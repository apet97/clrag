# oss-python-langgraph-local-server

> Source: https://docs.langchain.com/oss/python/langgraph/local-server

LangGraph v1.0Welcome to the new LangGraph documentation! If you encounter any issues or have feedback, please open an issue so we can improve. Archived v0 documentation can be found here.See the release notes and migration guide for a complete list of changes and instructions on how to upgrade your code.
Prerequisites
Before you begin, ensure you have the following:- An API key for LangSmith - free to sign up
1. Install the LangGraph CLI
2. Create a LangGraph app 🌱
Create a new app from thenew-langgraph-project-python
template. This template demonstrates a single-node application you can extend with your own logic.
Additional templates
If you use
langgraph new
without specifying a template, you will be presented with an interactive menu that will allow you to choose from a list of available templates.3. Install dependencies
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
- Python SDK (async)
- Python SDK (sync)
- Rest API
- Install the LangGraph Python SDK:
- Send a message to the assistant (threadless run):
Next steps
Now that you have a LangGraph app running locally, take your journey further by exploring deployment and advanced features:- Deployment quickstart: Deploy your LangGraph app using LangSmith.
- LangSmith: Learn about foundational LangSmith concepts.
- Python SDK Reference: Explore the Python SDK API Reference.