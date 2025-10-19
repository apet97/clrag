# langsmith-hybrid

> Source: https://docs.langchain.com/langsmith/hybrid

- Control plane (LangSmith UI, APIs, and orchestration) runs in LangChain’s cloud, managed by LangChain.
- Data plane (your and agent workloads) runs in your cloud, managed by you.
| Component | Responsibilities | Where it runs | Who manages it |
|---|---|---|---|
| LangChain’s cloud | LangChain | |
| Your cloud | You |
Workflow
- Use the
langgraph-cli
or Studio to test your graph locally. - Build a Docker image using the
langgraph build
command. - Deploy your LangGraph Server from the control plane UI.
Architecture
Compute Platforms
- Kubernetes: Hybrid supports running the data plane on any Kubernetes cluster.
Egress to LangSmith and the control plane
In the hybrid deployment model, your self-hosted data plane will send network requests to the control plane to poll for changes that need to be implemented in the data plane. Traces from data plane deployments also get sent to the LangSmith instance integrated with the control plane. This traffic to the control plane is encrypted, over HTTPS. The data plane authenticates with the control plane with a LangSmith API key. In order to enable this egress, you may need to update internal firewall rules or cloud resources (such as Security Groups) to allow certain IP addresses.AWS/Azure PrivateLink or GCP Private Service Connect is currently not supported. This traffic will go over the internet.
Listeners
In the hybrid option, one or more “listener” applications can run depending on how your LangSmith workspaces and Kubernetes clusters are organized.Kubernetes cluster organization
- One or more listeners can run in a Kubernetes cluster.
- A listener can deploy into one or more namespaces in that cluster.
- Cluster owners are responsible for planning listener layout and LangGraph Server deployments.
LangSmith workspace organization
- A workspace can be associated with one or more listeners.
- A workspace can only deploy to Kubernetes clusters where all of its listeners are deployed.
Use Cases
Here are some common listener configurations (not strict requirements):Each LangSmith workspace → separate Kubernetes cluster
- Cluster
alpha
runs workspaceA
- Cluster
beta
runs workspaceB
Separate clusters, with shared “dev” cluster
- Cluster
alpha
runs workspaceA
- Cluster
beta
runs workspaceB
- Cluster
dev
runs workspacesA
andB
- Both workspaces have two listeners; cluster
dev
has two listener deployments
One cluster, one namespace per workspace
- Cluster
alpha
, namespace1
runs workspaceA
- Cluster
alpha
, namespace2
runs workspaceB
One cluster, single namespace for multiple workspaces
- Cluster
alpha
runs workspaceA
- Cluster
alpha
runs workspaceB