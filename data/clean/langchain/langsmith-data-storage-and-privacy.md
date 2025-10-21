---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-data-storage-and-privacy",
  "h1": "langsmith-data-storage-and-privacy",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.471953",
  "sha256_raw": "7708425edcf1f89b3c0a5a3a862bffc87b774d753163c1c6935a2d286bfb3084"
}
---

# langsmith-data-storage-and-privacy

> Source: https://docs.langchain.com/langsmith/data-storage-and-privacy

langgraph dev
) and the local Docker server (langgraph up
). It also describes what data is tracked when interacting with the hosted Studio frontend.
CLI
LangGraph CLI is the command-line interface for building and running LangGraph applications; see the CLI guide to learn more. By default, calls to most CLI commands log a single analytics event upon invocation. This helps us better prioritize improvements to the CLI experience. Each telemetry event contains the calling process’s OS, OS version, Python version, the CLI version, the command name (dev
, up
, run
, etc.), and booleans representing whether a flag was passed to the command. You can see the full analytics logic here.
You can disable all CLI telemetry by setting LANGGRAPH_CLI_NO_ANALYTICS=1
.
LangGraph Server
The LangGraph Server provides a durable execution runtime that relies on persisting checkpoints of your application state, long-term memories, thread metadata, assistants, and similar resources to the local file system or a database. Unless you have deliberately customized the storage location, this information is either written to local disk (forlanggraph dev
) or a PostgreSQL database (for langgraph up
and in all deployments).
LangSmith Tracing
When running the LangGraph server (either in-memory or in Docker), LangSmith tracing may be enabled to facilitate faster debugging and offer observability of graph state and LLM prompts in production. You can always disable tracing by settingLANGSMITH_TRACING=false
in your server’s runtime environment.
In-memory development server
langgraph dev
runs an in-memory development server as a single Python process, designed for quick development and testing. It saves all checkpointing and memory data to disk within a .langgraph_api
directory in the current working directory. Apart from the telemetry data described in the CLI section, no data leaves the machine unless you have enabled tracing or your graph code explicitly contacts an external service.
Standalone Server
langgraph up
builds your local package into a Docker image and runs the server as the data plane consisting of three containers: the API server, a PostgreSQL container, and a Redis container. All persistent data (checkpoints, assistants, etc.) are stored in the PostgreSQL database. Redis is used as a pubsub connection for real-time streaming of events. You can encrypt all checkpoints before saving to the database by setting a valid LANGGRAPH_AES_KEY
environment variable. You can also specify TTLs for checkpoints and cross-thread memories in langgraph.json
to control how long data is stored. All persisted threads, memories, and other data can be deleted via the relevant API endpoints.
Additional API calls are made to confirm that the server has a valid license and to track the number of executed runs and tasks. Periodically, the API server validates the provided license key (or API key).
If you’ve disabled tracing, no user data is persisted externally unless your graph code explicitly contacts an external service.
Studio
Studio is a graphical interface for interacting with your LangGraph server. It does not persist any private data (the data you send to your server is not sent to LangSmith). Though the Studio interface is served at smith.langchain.com, it is run in your browser and connects directly to your local LangGraph server so that no data needs to be sent to LangSmith. If you are logged in, LangSmith does collect some usage analytics to help improve the debugging user experience. This includes:- Page visits and navigation patterns
- User actions (button clicks)
- Browser type and version
- Screen resolution and viewport size
Quick reference
In summary, you can opt-out of server-side telemetry by turning off CLI analytics and disabling tracing.| Variable | Purpose | Default |
|---|---|---|
LANGGRAPH_CLI_NO_ANALYTICS=1 | Disable CLI analytics | Analytics enabled |
LANGSMITH_API_KEY | Enable LangSmith tracing | Tracing disabled |
LANGSMITH_TRACING=false | Disable LangSmith tracing | Depends on environment |