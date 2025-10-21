---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-self-hosted",
  "h1": "langsmith-self-hosted",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.464663",
  "sha256_raw": "97463a51438d526d90a56be836bfbedc73914782c4efce56597979fe69a865db"
}
---

# langsmith-self-hosted

> Source: https://docs.langchain.com/langsmith/self-hosted

Important
Self-hosted LangSmith is an add-on to the Enterprise plan designed for our largest, most security-conscious customers. For more details, refer to Pricing. Contact our sales team if you want to get a license key to trial LangSmith in your environment.
Self-hosted LangSmith is an add-on to the Enterprise plan designed for our largest, most security-conscious customers. For more details, refer to Pricing. Contact our sales team if you want to get a license key to trial LangSmith in your environment.
- LangSmith: Deploy an instance of the LangSmith application that includes observability, tracing, and evaluations in the UI and API. Best for teams who want self-hosted monitoring and evaluation without deploying agents.
- LangSmith with deployment: Deploy a graph to LangGraph Server via the control plane. The control plane and data plane form the full LangSmith platform, providing UI and API management for running and monitoring agents. This includes observability, evaluation, and deployment management.
- Standalone server: Deploy a LangGraph Server directly without the control plane UI. Ideal for lightweight setups running one or a few agents as independent services, with full control over scaling and integration.
| Model | Includes | Best for | Methods |
|---|---|---|---|
| LangSmith |
|
|
|
| LangSmith with deployment |
|
|
|
| Standalone server |
|
|
|
LangSmith
Deploy an instance of the LangSmith application that includes observability, tracing, and evaluations in the UI and API—but without the ability to deploy agents through the control plane. This includes: Services:- LangSmith frontend UI
- LangSmith backend API
- LangSmith Platform backend
- LangSmith Playground
- LangSmith queue
- LangSmith ACE (Arbitrary Code Execution) backend
- ClickHouse (traces and feedback data)
- PostgreSQL (operational data)
- Redis (queuing and caching)
- Blob storage (optional, but recommended for production)
Services
Storage services
LangSmith will bundle all storage services by default. You can configure it to use external versions of all storage services. In a production setting, we strongly recommend using external storage services.
| Service | Description |
|---|---|
| ClickHouse | ClickHouse is a high-performance, column-oriented SQL database management system (DBMS) for online analytical processing (OLAP). LangSmith uses ClickHouse as the primary data store for traces and feedback (high-volume data). |
| PostgreSQL | PostgreSQL is a powerful, open source object-relational database system that uses and extends the SQL language combined with many features that safely store and scale the most complicated data workloads. LangSmith uses PostgreSQL as the primary data store for transactional workloads and operational data (almost everything besides traces and feedback). |
| Redis | Redis is a powerful in-memory key-value database that persists on disk. By holding data in memory, Redis offers high performance for operations like caching. LangSmith uses Redis to back queuing and caching operations. |
| Blob storage | LangSmith supports several blob storage providers, including AWS S3, Azure Blob Storage, and Google Cloud Storage. LangSmith uses blob storage to store large files, such as trace artifacts, feedback attachments, and other large data objects. Blob storage is optional, but highly recommended for production deployments. |
Setup methods
- Docker Compose (development/testing only)
- Kubernetes + Helm (recommended for production)
Setup guides
- Install on Kubernetes (production)
- Install with Docker (development only)
LangSmith with Deployment
LangSmith with deployment builds on top of the LangSmith option. Enabling deployment is ideal for enterprise teams who want a centralized, UI-driven platform to deploy and manage multiple agents and graphs, with all infrastructure, data, and orchestration fully under their control. This includes everything from LangSmith, plus:| Component | Responsibilities | Where it runs | Who manages it |
|---|---|---|---|
| Your cloud | You | |
| Your cloud | You |
Requirements
- You must already have a self-hosted LangSmith instance installed in your cloud
- Kubernetes cluster (required for control plane and data plane)
- Use
langgraph-cli
or Studio to test your graph locally - Build a Docker image with
langgraph build
- Deploy your LangGraph Server via the LangSmith control plane UI or through your container tooling of choice
- All agents are deployed as Kubernetes services behind the ingress configured for your LangSmith instance
Supported compute platforms
- Kubernetes: LangSmith with deployment supports running control plane and data plane infrastructure on any Kubernetes cluster.
Setup guide
Standalone Server
The Standalone server option is the most lightweight and flexible way to run LangSmith. Unlike the other models, you only manage a simplified made up of LangGraph Servers and their required backing services (PostgreSQL, Redis, etc.). This includes:| Component | Responsibilities | Where it runs | Who manages it |
|---|---|---|---|
| Control plane | n/a | n/a | n/a |
| Data plane |
| Your cloud | You |
Do not run standalone servers in serverless environments. Scale-to-zero may cause task loss and scaling up will not work reliably.
Workflow
- Define and test your graph locally using the
langgraph-cli
or Studio - Package your agent as a Docker image
- Deploy the LangGraph Server to your compute platform of choice (Kubernetes, Docker, VM)
- Optionally, configure LangSmith API keys and endpoints so the server reports traces and evaluations back to LangSmith (self-hosted or SaaS)
Supported compute platforms
- Kubernetes: Use the LangSmith Helm chart to run LangGraph Servers in a Kubernetes cluster. This is the recommended option for production-grade deployments.
- Docker: Run in any Docker-supported compute platform (local dev machine, VM, ECS, etc.). This is best suited for development or small-scale workloads.