# langsmith-deploy-hybrid

> Source: https://docs.langchain.com/langsmith/deploy-hybrid

Prerequisites
- Use the LangGraph CLI to test your application locally.
- Use the LangGraph CLI to build a Docker image (i.e.
langgraph build
) and push it to a registry your Kubernetes cluster or Amazon ECS cluster has access to.
Kubernetes
Prerequisites
KEDA
is installed on your cluster.- A valid
Ingress
controller is installed on your cluster. For more information about configuring ingress for your deployment, refer to Create an ingress for installations. - You have slack space in your cluster for multiple deployments.
Cluster-Autoscaler
is recommended to automatically provision new nodes. - You will need to enable egress to two control plane URLs. The listener polls these endpoints for deployments:
Setup
- Provide your LangSmith organization ID to us. Your LangSmith organization will be configured to deploy the data plane in your cloud.
- Create a listener from the LangSmith UI. The
Listener
data model is configured for the actual “listener” application.- In the left-hand navigation, select
Deployments
>Listeners
. - In the top-right of the page, select
+ Create Listener
. - Enter a unique
Compute ID
for the listener. TheCompute ID
is a user-defined identifier that should be unique across all listeners in the current LangSmith workspace. TheCompute ID
is displayed to end users when they are creating a new deployment. Ensure that theCompute ID
provides context to the end user about where their LangGraph Server deployments will be deployed to. For example, aCompute ID
can be set tok8s-cluster-name-dev-01
. In this example, the name of the Kubernetes cluster isk8s-cluster-name
,dev
denotes that the cluster is reserved for “development” workloads, and01
is a numerical suffix to reduce naming collisions. - Enter one or more Kubernetes namespaces. Later, the “listener” application will be configured to deploy to each of these namespaces.
- In the top-right on the page, select
Submit
. - After the listener is created, copy the listener ID. You will use it later when installing the actual “listener” application in the Kubernetes cluster (step 5).
Important Creating a listener from the LangSmith UI does not install the “listener” application in the Kubernetes cluster. - In the left-hand navigation, select
- A Helm chart is provided to install the necesssary components in your Kubernetes cluster.
langgraph-listener
: This is a service that listens to LangChain’s control plane for changes to your deployments and creates/updates downstream CRDs. This is the “listener” application.LangGraphPlatform CRD
: A CRD for LangSmith Deployment. This contains the spec for managing an instance of a LangSmith Deployment.langgraph-platform-operator
: This operator handles changes to your LangSmith CRDs.
- Configure your
langgraph-dataplane-values.yaml
file.config.langsmithApiKey
: Thelanggraph-listener
deployment authenticates with LangChain’s LangGraph control plane API with thelangsmithApiKey
.config.langsmithWorkspaceId
: Thelanggraph-listener
deployment is coupled to LangGraph Server deployments in the LangSmith workspace. In other words, thelanggraph-listener
deployment can only manage LangGraph Server deployments in the specified LangSmith workspace ID.config.langgraphListenerId
: In addition to being coupled with a LangSmith workspace, thelanggraph-listener
deployment is also coupled to a listener. When a new LangGraph Server deployment is created, it is automatically coupled to alanggraphListenerId
. SpecifyinglanggraphListenerId
ensures that thelanggraph-listener
deployment can only manage LangGraph Server deployments that are coupled tolanggraphListenerId
.config.watchNamespaces
: A comma-separated list of Kubernetes namespaces that thelanggraph-listener
deployment will deploy to. This list should match the list of namespaces specified in step 2d.config.enableLGPDeploymentHealthCheck
: To disable the LangGraph Server health check, set this tofalse
.ingress.hostname
: As part of the deployment workflow, thelanggraph-listener
deployment attempts to call the LangGraph Server health check endpoint (GET /ok
) to verify that the application has started up correctly. A typical setup involves creating a shared DNS record or domain for LangGraph Server deployments. This is not managed by LangSmith. Once created, setingress.hostname
to the domain, which will be used to complete the health check.operator.enabled
: There can only be 1 instance of thelanggraph-platform-operator
deployed in a Kubernetes namespace. Set this tofalse
if there is already an instance oflanggraph-platform-operator
deployed in the current Kubernetes namespace.operator.createCRDs
: Set this value tofalse
if the Kubernetes cluster already has theLangGraphPlatform CRD
installed. During installation, an error will occur if the CRD is already installed. This situation may occur if multiple listeners are deployed on the same Kubernetes cluster.
- Deploy
langgraph-dataplane
Helm chart. - If successful, you will see three services start up in your namespace.
- Create a deployment from the control plane UI.
- Select the desired listener from the list of
Compute IDs
in the dropdown menu. - Select the Kubernetes namespace to deploy to.
- Fill out all other required fields and select
Submit
in the top-right of the panel. - The deployment will be deployed on the Kubernetes cluster where the listener is deployed and in the Kubernetes namespace specified in step 7b.
- Select the desired listener from the list of