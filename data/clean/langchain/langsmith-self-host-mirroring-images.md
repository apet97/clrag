---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-self-host-mirroring-images",
  "h1": "langsmith-self-host-mirroring-images",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.477183",
  "sha256_raw": "b8d91c96b986b891768b60e2e13c7b69fba7ee4b1e723816a620cf0cd867384b"
}
---

# langsmith-self-host-mirroring-images

> Source: https://docs.langchain.com/langsmith/self-host-mirroring-images

By default, LangSmith will pull images from our public Docker registry. However, if you are running LangSmith in an environment that does not have internet access, or if you would like to use a private Docker registry, you can mirror the images to your own registry and then configure your LangSmith installation to use those images.
For your convenience, we have provided a script that will mirror the images for you. You can find the script in the LangSmith Helm Chart repositoryTo use the script, you will need to run the script with the following command specifying your registry and platform:
Where <your-registry> is the URL of your Docker registry (e.g. myregistry.com) and <platform> is the platform you are using (e.g. linux/amd64, linux/arm64, etc.). If you do not specify a platform, it will default to linux/amd64.For example, if your registry is myregistry.com, your platform is linux/arm64, and you want to use the latest version of the images, you would run:
Note that this script will assume that you have Docker installed and that you are authenticated to your registry. It will also push the images to the specified registry with the same repository/tag as the original images.Alternatively, you can pull, mirror, and push the images manually. The images that you will need to mirror are found in the values.yaml file of the LangSmith Helm Chart. These can be found here: LangSmith Helm Chart values.yamlHere is an example of how to mirror the images using Docker:
Copy
# Pull the images from the public registrydocker pull langchain/langsmith-backend:latestdocker tag langchain/langsmith-backend:latest <your-registry>/langsmith-backend:latestdocker push <your-registry>/langsmith-backend:latest
You will need to repeat this for each image that you want to mirror.
Once the images are mirrored, you will need to configure your LangSmith installation to use the mirrored images. You can do this by modifying the values.yaml file for your LangSmith Helm Chart installation or the .env file for your Docker installation. Replace tag with the version you want to use, e.g. 0.10.66 for the latest version at the time of writing.
Copy
images: imagePullSecrets: [] # Add your image pull secrets here if needed registry: "" # Set this to your registry URL if you mirrored all images to the same registry using our script. Then you can remove the repository prefix from the images below. aceBackendImage: repository: "(your-registry)/langchain/langsmith-ace-backend" pullPolicy: IfNotPresent tag: "0.10.66" backendImage: repository: "(your-registry)/langchain/langsmith-backend" pullPolicy: IfNotPresent tag: "0.10.66" frontendImage: repository: "(your-registry)/langchain/langsmith-frontend" pullPolicy: IfNotPresent tag: "0.10.66" hostBackendImage: repository: "(your-registry)/langchain/hosted-langserve-backend" pullPolicy: IfNotPresent tag: "0.10.66" operatorImage: repository: "(your-registry)/langchain/langgraph-operator" pullPolicy: IfNotPresent tag: "6cc83a8" platformBackendImage: repository: "(your-registry)/langchain/langsmith-go-backend" pullPolicy: IfNotPresent tag: "0.10.66" playgroundImage: repository: "(your-registry)/langchain/langsmith-playground" pullPolicy: IfNotPresent tag: "0.10.66" postgresImage: repository: "(your-registry)/postgres" pullPolicy: IfNotPresent tag: "14.7" redisImage: repository: "(your-registry)/redis" pullPolicy: IfNotPresent tag: "7" clickhouseImage: repository: "(your-registry)/clickhouse/clickhouse-server" pullPolicy: Always tag: "24.8"
Once configured, you will need to update your LangSmith installation. You can follow our upgrade guide here: Upgrading LangSmith.If your upgrade is successful, your LangSmith instance should now be using the mirrored images from your Docker registry.