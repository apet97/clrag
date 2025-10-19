# langsmith-hosting

> Source: https://docs.langchain.com/langsmith/hosting

Choose your hosting option
You’ll deploy LangSmith in one of three modes:- Cloud: fully managed by LangChain
- Hybrid: LangChain manages the ; you host the
- Self-hosted: you manage the full stack within your infrastructure
Cloud
Run all components fully managed in LangChain’s cloud.
Hybrid
(Enterprise) Manage the data plane running in your cloud while LangChain manages the control plane.
Self-hosted
(Enterprise) Run the full LangSmith or run standalone LangGraph Servers without the control plane UI.
Comparison
Refer to the following table for a comparison of hosting options:| Feature | Cloud | Hybrid | Self-Hosted |
|---|---|---|---|
| Infrastructure location | LangChain’s cloud | Split: Control plane in LangChain cloud, data plane in your cloud | Your cloud |
| Who manages updates | LangChain | LangChain (control plane), You (data plane) | You |
| Who manages CI/CD for your apps | LangChain | You | You |
| Can deploy applications? | ✅ Yes | ✅ Yes | ✅ Yes (with full platform option) |
| Observability data location | LangChain cloud | LangChain cloud | Your cloud |
| Pricing | Plus tier | Enterprise | Enterprise |
| Best for | Quick setup, managed infrastructure | Data residency requirements + managed control plane | Full control, data isolation |