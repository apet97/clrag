# langsmith-self-host-ingress

> Source: https://docs.langchain.com/langsmith/self-host-ingress

langsmith-frontend
. Depending on your cloud provider, this may result in a public IP address being assigned to the service. If you would like to use a custom domain or have more control over the routing of traffic to your LangSmith installation, you can configure an Ingress.
Requirements
- An existing Kubernetes cluster
- An existing Ingress Controller installed in your Kubernetes cluster
Parameters
You may need to provide certain parameters to your LangSmith installation to configure the Ingress. Additionally, we will want to convert thelangsmith-frontend
service to a ClusterIP service.
-
Hostname (optional): The hostname that you would like to use for your LangSmith installation. E.g
"langsmith.example.com"
. If you leave this empty, the ingress will serve all traffic to the LangSmith installation. -
Subdomain (optional): If you would like to serve LangSmith under a URL path, you can specify it here. For example, adding
"langsmith"
will serve the application at"example.hostname.com/langsmith"
. This will apply to UI paths as well as API endpoints. - IngressClassName (optional): The name of the Ingress class that you would like to use. If not set, the default Ingress class will be used.
-
Annotations (optional): Additional annotations to add to the Ingress. Certain providers like AWS may use annotations to control things like TLS termination.
For example, you can add the following annotations using the AWS ALB Ingress Controller to attach an ACM certificate to the Ingress:
- Labels (optional): Additional labels to add to the Ingress.
-
TLS (optional): If you would like to serve LangSmith over HTTPS, you can add TLS configuration here (many Ingress controllers may have other ways of controlling TLS so this is often not needed). This should be an array of TLS configurations. Each TLS configuration should have the following fields:
- hosts: An array of hosts that the certificate should be valid for. E.g [“langsmith.example.com”]
-
secretName: The name of the Kubernetes secret that contains the certificate and private key. This secret should have the following keys:
- tls.crt: The certificate
- tls.key: The private key
- You can read more about creating a TLS secret here.
Configuration
With these parameters in hand, you can configure your LangSmith instance to use an Ingress. You can do this by modifying theconfig.yaml
file for your LangSmith Helm Chart installation.
If you do not have automated DNS setup, you will need to add the IP address to your DNS provider manually.