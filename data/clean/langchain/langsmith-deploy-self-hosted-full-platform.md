---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-deploy-self-hosted-full-platform",
  "h1": "langsmith-deploy-self-hosted-full-platform",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.476227",
  "sha256_raw": "2f8c8c9f707f87271eb05d1f60f4440c030e2377e71f8f6aa78865d98245a864"
}
---

# langsmith-deploy-self-hosted-full-platform

> Source: https://docs.langchain.com/langsmith/deploy-self-hosted-full-platform

This setup page is for adding deployment capabilities to an existing LangSmith instance.Review the self-hosted options to understand:
- LangSmith (observability): What you should install first.
- LangSmith with deployment: What this guide enables.
- Standalone Server: Lightweight alternative without the UI.
Overview
This guide builds on top of the Kubernetes installation guide. You must complete that guide first before continuing. This page covers the additional setup steps required to enable deployment functionality:- Installing the LangGraph operator
- Configuring your ingress
- Connecting to the control plane
Prerequisites
- You are using Kubernetes.
- You have an instance of self-hosted LangSmith running.
- Use the LangGraph CLI to test your application locally.
- Use the LangGraph CLI to build a Docker image (i.e.
langgraph build
) and push it to a registry your Kubernetes cluster has access to. KEDA
is installed on your cluster.
- Ingress Configuration
- You must set up an ingress for your LangSmith instance. All agents will be deployed as Kubernetes services behind this ingress. Use this guide to set up an ingress for your instance.
- You have slack space in your cluster for multiple deployments.
Cluster-Autoscaler
is recommended to automatically provision new nodes. - A valid Dynamic PV provisioner or PVs available on your cluster. You can verify this by running:
- Egress to
https://beacon.langchain.com
from your network. This is required for license verification and usage reporting if not running in air-gapped mode. See the Egress documentation for more details.
Setup
- As part of configuring your self-hosted LangSmith instance, you enable the
langgraphPlatform
option. This will provision a few key resources.listener
: This is a service that listens to the control plane for changes to your deployments and creates/updates downstream CRDs.LangGraphPlatform CRD
: A CRD for LangSmith Deployment. This contains the spec for managing an instance of a LangSmith deployment.operator
: This operator handles changes to your LangSmith CRDs.host-backend
: This is the control plane.
- Two additional images will be used by the chart. Use the images that are specified in the latest release.
- In your config file for langsmith (usually
langsmith_config.yaml
), enable thelanggraphPlatform
option. Note that you must also have a valid ingress setup:
- In your
values.yaml
file, configure thehostBackendImage
andoperatorImage
options (if you need to mirror images) - You can also configure base templates for your agents by overriding the base templates here.
- You create a deployment from the control plane UI.