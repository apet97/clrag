# langsmith-bind-evaluator-to-dataset

> Source: https://docs.langchain.com/langsmith/bind-evaluator-to-dataset

- Programmatically, by specifying evaluators in your code (see this guide for details)
- By binding evaluators to a dataset in the UI. This will automatically run the evaluators on any new experiments created, in addition to any evaluators you’ve set up via the SDK. This is useful when you’re iterating on your application (target function), and have a standard set of evaluators you want to run for all experiments.
Configuring an evaluator on a dataset
- Click on the Datasets and Experiments tab in the sidebar.
- Select the dataset you want to configure the evaluator for.
- Click on the + Evaluator button to add an evaluator to the dataset. This will open a pane you can use to configure the evaluator.
When you configure an evaluator for a dataset, it will only affect the experiment runs that are created after the evaluator is configured. It will not affect the evaluation of experiment runs that were created before the evaluator was configured.
LLM-as-a-judge evaluators
The process for binding evaluators to a dataset is very similar to the process for configuring a LLM-as-a-judge evaluator in the Playground. View instructions for configuring an LLM-as-a-judge evaluator in the Playground.Custom code evaluators
The process for binding a code evaluators to a dataset is very similar to the process for configuring a code evaluator in online evaluation. View instruction for configuring code evaluators. The only difference between configuring a code evaluator in online evaluation and binding a code evaluator to a dataset is that the custom code evaluator can reference outputs that are part of the dataset’sExample
.
For custom code evaluators bound to a dataset, the evaluator function takes in two arguments:
- A
Run
(reference). This represents the new run in your experiment. For example, if you ran an experiment via SDK, this would contain the input/output from your chain or model you are testing. - An
Example
(reference). This represents the reference example in your dataset that the chain or model you are testing uses. Theinputs
to the Run and Example should be the same. If your Example has a referenceoutputs
, then you can use this to compare to the run’s output for scoring.
Next steps
- Analyze your experiment results in the experiments tab
- Compare your experiment results in the comparison view