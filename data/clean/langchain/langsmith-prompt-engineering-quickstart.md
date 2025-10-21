---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-prompt-engineering-quickstart",
  "h1": "langsmith-prompt-engineering-quickstart",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.457200",
  "sha256_raw": "e42fbdf8e9624649f00dc6a39591486d989f3ceab4b132a023377ea6e3bc501e"
}
---

# langsmith-prompt-engineering-quickstart

> Source: https://docs.langchain.com/langsmith/prompt-engineering-quickstart

Prerequisites
Before you begin, make sure you have:- A LangSmith account: Sign up or log in at smith.langchain.com.
- A LangSmith API key: Follow the Create an API key guide.
- An OpenAI API key: Generate this from the OpenAI dashboard.
- UI
- SDK
1. Set workspace secret
In the LangSmith UI, ensure that your OpenAI API key is set as a workspace secret.- Navigate to Settings and then move to the Secrets tab.
- Select Add secret and enter the
OPENAI_API_KEY
and your API key as the Value. - Select Save secret.
When adding workspace secrets in the LangSmith UI, make sure the secret keys match the environment variable names expected by your model provider.
2. Create a prompt
- In the LangSmith UI, navigate to the Prompts section in the left-hand menu.
- Click on + Prompt to create a prompt.
- Modify the prompt by editing or adding prompts and input variables as needed.
3. Test a prompt
- Under the Prompts heading select the gear icon next to the model name, which will launch the Prompt Settings window on the Model Configuration tab.
-
Set the model configuration you want to use. The Provider and Model you select will determine the parameters that are configurable on this configuration page. Once set, click Save as.
-
Specify the input variables you would like to test in the Inputs box and then click Start.
To learn about more options for configuring your prompt in the Playground, refer to Configure prompt settings.
- After testing and refining your prompt, click Save to store it for future use.
4. Iterate on a prompt
LangSmith allows for team-based prompt iteration. Workspace members can experiment with prompts in the playground and save their changes as a new commit when ready.To improve your prompts:- Reference the documentation provided by your model provider for best practices in prompt creation, such as:
- Build and refine your prompts with the Prompt Canvas—an interactive tool in LangSmith. Learn more in the Prompt Canvas guide.
-
Tag specific commits to mark important moments in your commit history.
- To create a commit, navigate to the Playground and select Commit. Choose the prompt to commit changes to and then Commit.
- Navigate to Prompts in the left-hand menu. Select the prompt. Once on the prompt’s detail page, move to the Commits tab. Find the tag icon to Add a Commit Tag.
Next steps
- Learn more about how to store and manage prompts using the Prompt Hub in the Create a prompt guide.
- Learn how to set up the Playground to Test multi-turn conversations in this tutorial.
- Learn how to test your prompt’s performance over a dataset instead of individual examples, refer to Run an evaluation from the Prompt Playground.