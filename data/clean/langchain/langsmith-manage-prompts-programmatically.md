---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-manage-prompts-programmatically",
  "h1": "langsmith-manage-prompts-programmatically",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.474693",
  "sha256_raw": "910da8070dc945ac0d6ac24db14735d1c08e3382951a85095a9764bd5a720215"
}
---

# langsmith-manage-prompts-programmatically

> Source: https://docs.langchain.com/langsmith/manage-prompts-programmatically

Previously this functionality lived in the
langchainhub
package which is now deprecated. All functionality going forward will live in the langsmith
package.Install packages
In Python, you can directly use the LangSmith SDK (recommended, full functionality) or you can use through the LangChain package (limited to pushing and pulling prompts). In TypeScript, you must use the LangChain npm package for pulling prompts (it also allows pushing). For all other functionality, use the LangSmith package.Configure environment variables
If you already haveLANGSMITH_API_KEY
set to your current workspace’s api key from LangSmith, you can skip this step.
Otherwise, get an API key for your workspace by navigating to Settings > API Keys > Create API Key
in LangSmith.
Set your environment variable.
What we refer to as “prompts” used to be called “repos”, so any references to “repo” in the code are referring to a prompt.
Push a prompt
To create a new prompt or update an existing prompt, you can use thepush prompt
method.
Pull a prompt
To pull a prompt, you can use thepull prompt
method, which returns a the prompt as a langchain PromptTemplate
.
To pull a private prompt you do not need to specify the owner handle (though you can, if you have one set).
To pull a public prompt from the LangChain Hub, you need to specify the handle of the prompt’s author.
For pulling prompts, if you are using Node.js or an environment that supports dynamic imports, we recommend using the
langchain/hub/node
entrypoint, as it handles deserialization of models associated with your prompt configuration automatically.If you are in a non-Node environment, “includeModel” is not supported for non-OpenAI models and you should use the base langchain/hub
entrypoint.Use a prompt without LangChain
If you want to store your prompts in LangSmith but use them directly with a model provider’s API, you can use our conversion methods. These convert your prompt into the payload required for the OpenAI or Anthropic API. These conversion methods rely on logic from within LangChain integration packages, and you will need to install the appropriate package as a dependency in addition to your official SDK of choice. Here are some examples:OpenAI
Anthropic
List, delete, and like prompts
You can also list, delete, and like/unlike prompts using thelist prompts
, delete prompt
, like prompt
and unlike prompt
methods. See the LangSmith SDK client for extensive documentation on these methods.