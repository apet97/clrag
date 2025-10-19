# langsmith-components

> Source: https://docs.langchain.com/langsmith/components

When running the self-hosted LangSmith with deployment, your installation includes several key components. Together these tools and services provide a complete solution for building, deploying, and managing graphs (including agentic applications) in your own infrastructure:
LangGraph Server: Defines an opinionated API and runtime for deploying graphs and agents. Handles execution, state management, and persistence so you can focus on building logic rather than server infrastructure.
LangGraph CLI: A command-line interface to build, package, and interact with graphs locally and prepare them for deployment.
Studio: A specialized IDE for visualization, interaction, and debugging. Connects to a local LangGraph Server for developing and testing your graph.
Python/JS SDK: The Python/JS SDK provides a programmatic way to interact with deployed graphs and agents from your applications.
RemoteGraph: Allows you to interact with a deployed graph as though it were running locally.
Control Plane: The UI and APIs for creating, updating, and managing LangGraph Server deployments.
Data plane: The runtime layer that executes your graphs, including LangGraph Servers, their backing services (PostgreSQL, Redis, etc.), and the listener that reconciles state from the control plane.