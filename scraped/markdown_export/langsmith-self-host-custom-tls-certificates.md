# langsmith-self-host-custom-tls-certificates

> Source: https://docs.langchain.com/langsmith/self-host-custom-tls-certificates

- Mounting internal certificate authorities (CAs) system-wide to enable TLS for database connections and Playground model calls
- Using Playground-specific TLS settings to provide client certs/keys for mTLS with supported model providers
Mount internal CAs for TLS
You must use Helm chart version 0.11.9 or later to mount internal CAs using the configuration below.
- Create a file containing all CAs required for TLS with databases and external services. If your deployment is communicating directly to
beacon.langchain.com
without a proxy, make sure to include a public trusted CA. All certs should be concatenated in this file with an empty line in between. - Create a Kubernetes secret with a key containing the contents of this file.
- If using custom CA for TLS with your databases and other external services, provide the following values to your LangSmith helm chart:
Helm
- Make sure to use TLS supported connection strings:
- Postgres: Add
?sslmode=verify-full&sslrootcert=system
to the end. - Redis: Use
rediss://
instead ofredis://
as the prefix.
- Postgres: Add
Use custom TLS certificates for model providers
This feature is currently only available for the following model providers:
- Azure OpenAI
- OpenAI
- Custom (our custom model server). Refer to the custom model server documentation for more information.
LANGSMITH_PLAYGROUND_TLS_MODEL_PROVIDERS
: A comma-separated list of model providers that require custom TLS certificates. Note thatazure_openai
,openai
, andcustom
are currently the only supported model providers, but more providers will be supported in the future.- [Optional]
LANGSMITH_PLAYGROUND_TLS_KEY
: The private key in PEM format. This must be a file path (for a mounted volume). This is usually only necessary for mutual TLS authentication. - [Optional]
LANGSMITH_PLAYGROUND_TLS_CERT
: The certificate in PEM format. This must be a file path (for a mounted volume). This is usually only necessary for mutual TLS authentication. - [Optional]
LANGSMITH_PLAYGROUND_TLS_CA
: The custom certificate authority (CA) certificate in PEM format. This must be a file path (for a mounted volume). Use this to mount CAs only if you’re using a helm version below0.11.9
; otherwise, use the Mount internal CAs for TLS section above.