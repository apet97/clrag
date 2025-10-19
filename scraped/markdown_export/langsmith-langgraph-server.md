# langsmith-langgraph-server

> Source: https://docs.langchain.com/langsmith/langgraph-server

To use the
Enterprise
version of the LangGraph Server, you must acquire a license key that you will need to specify when running the Docker image. To acquire a license key, contact our sales team.
You can run the Enterprise
version of the LangGraph Server on the following deployment options:
- Cloud
- Hybrid
- Self-hosted
Application structure
To deploy a LangGraph Server application, you need to specify the graph(s) you want to deploy, as well as any relevant configuration settings, such as dependencies and environment variables. Read the application structure guide to learn how to structure your LangGraph application for deployment.Parts of a deployment
When you deploy LangGraph Server, you are deploying one or more graphs, a database for persistence, and a task queue.Graphs
When you deploy a graph with LangGraph Server, you are deploying a “blueprint” for an Assistant. An Assistant is a graph paired with specific configuration settings. You can create multiple assistants per graph, each with unique settings to accommodate different use cases that can be served by the same graph. Upon deployment, LangGraph Server will automatically create a default assistant for each graph using the graph’s default configuration settings.We often think of a graph as implementing an agent, but a graph does not necessarily need to implement an agent. For example, a graph could implement a simple
chatbot that only supports back-and-forth conversation, without the ability to influence any application control flow. In reality, as applications get more complex, a graph will often implement a more complex flow that may use multiple agents working in tandem.
Persistence and task queue
LangGraph Server leverages a database for persistence and a task queue. PostgreSQL is supported as a database for LangGraph Server and Redis as the task queue. If you’re deploying using LangSmith cloud, these components are managed for you. If you’re deploying LangGraph Server on your own infrastructure, you’ll need to set up and manage these components yourself. For more information on how these components are set up and managed, review the hosting options guide.Learn more
- LangGraph Application Structure guide explains how to structure your LangGraph application for deployment.
- The API Reference provides detailed information on the API endpoints and data models.