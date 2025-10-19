# langsmith-kubernetes

> Source: https://docs.langchain.com/langsmith/kubernetes

Self-hosting LangSmith is an add-on to the Enterprise Plan designed for our largest, most security-conscious customers. See our pricing page for more detail, and contact our sales team if you want to get a license key to trial LangSmith in your environment.
This guide installs the base LangSmith platform which includes observability and evaluation, but not the deployment management features. Review the self-hosted options if you’re unsure which you need.
- ✅ LangSmith UI and APIs: for observability, tracing, and evaluation.
- ✅ Backend services: (queue, playground, ACE).
- ✅ Datastores: (PostgreSQL, Redis, ClickHouse, optional blob storage).
- ❌ Deployment management: To add deployment capabilities, complete this guide first, then follow Self-host LangSmith with deployment.
- Google Kubernetes Engine (GKE)
- Amazon Elastic Kubernetes Service (EKS)
- Azure Kubernetes Service (AKS)
- OpenShift (4.14+)
- Minikube and Kind (for development purposes)
We have several Terraform modules the help in the provisioning of resources for LangSmith. You can find those in our public Terraform repo.Supported cloud providers include:You can click on the links above to see the documentation for each module. These modules are designed to help you quickly set up the necessary infrastructure for LangSmith, including Kubernetes clusters, storage, and networking.
Prerequisites
Ensure you have the following tools/items ready. Some items are marked optional:-
LangSmith License Key
- You can get this from your LangChain representative. Contact our sales team for more information.
-
Api Key Salt
- This is a secret key that you can generate. It should be a random string of characters.
- You can generate this using the following command:
-
JWT Secret (Optional but used for basic auth)
- This is a secret key that you can generate. It should be a random string of characters.
- You can generate this using the following command:
Databases
LangSmith uses a PostgreSQL database, a Redis cache, and a ClickHouse database to store traces. By default, these services are installed inside your Kubernetes cluster. However, we highly recommend using external databases instead. For PostgreSQL and Redis, the best option is your cloud provider’s managed services. For more information, refer to the following setup guides for external services:Kubernetes cluster requirements
-
You will need a working Kubernetes cluster that you can access via
kubectl
. Your cluster should have the following minimum requirements:-
Recommended: At least 16 vCPUs, 64GB Memory available
- You may need to tune resource requests/limits for all of our different services based off of organization size/usage. Our recommendations can be found here.
- We recommend using a cluster autoscaler to handle scaling up/down of nodes based on resource usage.
- We recommend setting up the metrics server so that autoscaling can be turned on.
- If you are running Clickhouse in-cluster, you must have a node with at least 4 vCPUs and 16GB of memory allocatable as ClickHouse will request this amount of resources by default.
-
Valid Dynamic PV provisioner or PVs available on your cluster (required only if you are running databases in-cluster)
- To enable persistence, we will try to provision volumes for any database running in-cluster.
- If using PVs in your cluster, we highly recommend setting up backups in a production environment.
- We strongly encourage using a storage class backed by SSDs for better performance. We recommend 7000 IOPS and 1000 MiB/s throughput.
- On EKS, you may need to ensure you have the
ebs-csi-driver
installed and configured for dynamic provisioning. Refer to the EBS CSI Driver documentation for more information.
The output should show at least one storage class with a provisioner that supports dynamic provisioning. For example:Refer to the Kubernetes documentation for more information on storage classes.We highly recommend using a storage class that supports volume expansion. This is because traces can potentially require a lot of disk space and your volumes may need to be resized over time.
-
Recommended: At least 16 vCPUs, 64GB Memory available
-
Helm
- To install
helm
refer to the Helm documentation
- To install
-
Egress to
https://beacon.langchain.com
(if not running in offline mode)- LangSmith requires egress to
https://beacon.langchain.com
for license verification and usage reporting. This is required for LangSmith to function properly. You can find more information on egress requirements in the Egress section.
- LangSmith requires egress to
Configure your Helm Charts:
-
Create a new file called
langsmith_config.yaml
with the configuration options from the previous step.- There are several configuration options that you can set in the
langsmith_config.yaml
file. You can find more information on specific configuration options in the Configuration section. - If you are new to Kubernetes or Helm, we’d recommend starting with one of the example configurations in the examples directory of the Helm Chart repository here: LangSmith helm chart examples.
- You can see a full list of configuration options in the
values.yaml
file in the Helm Chart repository here: LangSmith Helm Chart
- There are several configuration options that you can set in the
-
At a minimum, you will need to set the following configuration options (using basic auth):
Deploying to Kubernetes:
-
Verify that you can connect to your Kubernetes cluster(note: We highly suggest installing into an empty namespace)
-
Run
kubectl get pods
Output should look something like:
If you are using a namespace other than the default namespace, you will need to specify the namespace in thehelm
andkubectl
commands by using the-n <namespace>
flag. -
Run
-
Ensure you have the LangChain Helm repo added. (skip this step if you are using local charts)
-
Find the latest version of the chart. You can find the available versions in the Helm Chart repository.
- We generally recommend using the latest version.
- You can also run
helm search repo langchain/langsmith --versions
to see the available versions. The output will look something like this:
-
Run
helm upgrade -i langsmith langchain/langsmith --values langsmith_config.yaml --version <version> -n <namespace> --wait --debug
- Replace
<namespace>
with the namespace you want to deploy LangSmith to. - Replace
<version>
with the version of LangSmith you want to install from the previous step. Most users should install the latest version available.
helm install
command runs and finishes successfully, you should see output similar to this:This may take a few minutes to complete as it will create several Kubernetes resources and run several jobs to initialize the database and other services. - Replace
-
Run
kubectl get pods
Output should now look something like this (note the exact pod names may vary based on the version and configuration you used):
Validate your deployment:
-
Run
kubectl get services
Output should look something like: -
Curl the external ip of the
langsmith-frontend
service:Expected output: -
Visit the external ip for the
langsmith-frontend
service on your browser The LangSmith UI should be visible/operational
Using LangSmith
Now that LangSmith is running, you can start using it to trace your code. You can find more information on how to use self-hosted LangSmith in the self-hosted usage guide. Your LangSmith instance is now running but may not be fully setup yet. If you used one of the basic configs, you will have a default admin user account created for you. You can log in with the email address and password you specified in thelangsmith_config.yaml
file.
As a next step, it is strongly recommended you work with your infrastructure administrators to:
- Setup DNS for your LangSmith instance to enable easier access
- Configure SSL to ensure in-transit encryption of traces submitted to LangSmith
- Configure LangSmith with Single Sign-On to secure your LangSmith instance
- Connect LangSmith to external Postgres and Redis instances
- Set up Blob Storage for storing large files