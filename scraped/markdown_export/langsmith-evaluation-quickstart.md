# langsmith-evaluation-quickstart

> Source: https://docs.langchain.com/langsmith/evaluation-quickstart

- Dataset: A set of test inputs (and optionally, expected outputs).
- Target function: The part of your application you want to test—this might be a single LLM call with a new prompt, one module, or your entire workflow.
- Evaluators: Functions that score your target function’s outputs.
Prerequisites
Before you begin, make sure you have:- A LangSmith account: Sign up or log in at smith.langchain.com.
- A LangSmith API key: Follow the Create an API key guide.
- An OpenAI API key: Generate this from the OpenAI dashboard.
- UI
- SDK
1. Set workspace secrets
In the LangSmith UI, ensure that your OpenAI API key is set as a workspace secret.- Navigate to Settings and then move to the Secrets tab.
- Select Add secret and enter the
OPENAI_API_KEY
and your API key as the Value. - Select Save secret.
When adding workspace secrets in the LangSmith UI, make sure the secret keys match the environment variable names expected by your model provider.
2. Create a prompt
LangSmith’s Prompt Playground makes it possible to run evaluations over different prompts, new models, or test different model configurations.- In the LangSmith UI, navigate to the Playground under Prompt Engineering.
-
Under the Prompts panel, modify the system prompt to:
Leave the Human message as is:
{question}
.
3. Create a dataset
- Click Set up Evaluation, which will open a New Experiment table at the bottom of the page.
-
In the Select or create a new dataset dropdown, click the + New button to create a new dataset.
-
Add the following examples to the dataset:
Inputs Reference Outputs question: Which country is Mount Kilimanjaro located in? output: Mount Kilimanjaro is located in Tanzania. question: What is Earth’s lowest point? output: Earth’s lowest point is The Dead Sea. - Click Save and enter a name to save your newly created dataset.
4. Add an evaluator
- Click + Evaluator and select Correctness from the Pre-built Evaluator options.
- In the Correctness panel, click Save.
5. Run your evaluation
-
Select Start on the top right to run your evaluation. This will create an experiment with a preview in the New Experiment table. You can view in full by clicking the experiment name.
Next steps
- For more details on evaluations, refer to the Evaluation documentation.
- Learn how to create and manage datasets in the UI.
- Learn how to run an evaluation from the prompt playground.