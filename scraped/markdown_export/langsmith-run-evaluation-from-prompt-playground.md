# langsmith-run-evaluation-from-prompt-playground

> Source: https://docs.langchain.com/langsmith/run-evaluation-from-prompt-playground

LangSmith allows you to run evaluations directly in the UI. The Prompt Playground allows you to test your prompt or model configuration over a series of inputs to see how well it scores across different contexts or scenarios, without having to write any code.Before you run an evaluation, you need to have an existing dataset. Learn how to create a dataset from the UI.If you prefer to run experiments in code, visit run an evaluation using the SDK.
Navigate to the playground by clicking Playground in the sidebar.
Add a prompt by selecting an existing saved a prompt or creating a new one.
Select a dataset from the Test over dataset dropdown
Note that the keys in the dataset input must match the input variables of the prompt. For example, in the above video the selected dataset has inputs with the key “blog”, which correctly match the input variable of the prompt.
There is a maximum of 15 input variables allowed in the prompt playground.
Start the experiment by clicking on the Start or CMD+Enter. This will run the prompt over all the examples in the dataset and create an entry for the experiment in the dataset details page. We recommend committing the prompt to the prompt hub before starting the experiment so that it can be easily referenced later when reviewing your experiment.
View the full results by clicking View full experiment. This will take you to the experiment details page where you can see the results of the experiment.
Evaluate your experiment over specific critera by adding evaluators. Add LLM-as-a-judge or custom code evaluators in the playground using the +Evaluator button.To learn more about adding evaluators in via UI, visit how to define an LLM-as-a-judge evaluator.