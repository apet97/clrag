# langsmith-troubleshooting-variable-caching

> Source: https://docs.langchain.com/langsmith/troubleshooting-variable-caching

If you’re not seeing traces in your tracing project or notice traces logged to the wrong project/workspace, the issue might be due to LangSmith’s default environment variable caching. This is especially common when running LangSmith within a Jupyter notebook. Follow these steps to diagnose and resolve the issue:
Reload your environment variables from the .env file by executing:
Copy
from dotenv import load_dotenvimport osload_dotenv(<path to .env file>, override=True)
After reloading, your environment variables should be set correctly.If you continue to experience issues, please reach out to us via a shared Slack channel or email support (available for Plus and Enterprise plans), or in the LangChain Forum.