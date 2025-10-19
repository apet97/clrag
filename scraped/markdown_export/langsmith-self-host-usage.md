# langsmith-self-host-usage

> Source: https://docs.langchain.com/langsmith/self-host-usage

After setting the above, you should be able to run your code and see the results in your self-hosted instance. We recommend running through the quickstart guide to get a feel for how to use LangSmith.
If you are using self-signed certificates for your self-hosted LangSmith instance, this can be problematic as Python comes with its own set of trusted certificates, which may not include your self-signed certificate. To resolve this, you may need to use something like truststore to load system certificates into your Python environment.You can do this like so:
pip install truststore (or similar depending on the package manager you are using)
Then use the following code to load the system certificates:
Copy
import truststoretruststore.inject_into_ssl()# The rest of your codeimport langsmithlangsmith_client = langsmith.Client( api_key='<api_key>', api_url='http(s)://<host>/api/v1',)