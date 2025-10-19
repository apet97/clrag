# langsmith-online-evaluations

> Source: https://docs.langchain.com/langsmith/online-evaluations

Online evaluations provide real-time feedback on your production traces. This is useful to continuously monitor the performance of your application—to identify issues, measure improvements, and ensure consistent quality over time.
There are two types of online evaluations supported in LangSmith:
- LLM-as-a-judge: Use an LLM to evaluate your traces. Used as a scalable way to provide human-like judgement to your output (e.g. toxicity, hallucination, correctness, etc.).
- Custom Code: Write an evaluator in Python directly in LangSmith. Often used for validating structure or statistical properties of your data.
View online evaluators
Head to the Tracing Projects tab and select a tracing project. To view existing online evaluators for that project, click on the Evaluators tab.Configure online evaluators
1. Navigate to online evaluators
Head to the Tracing Projects tab and select a tracing project. Click on + New in the top right corner of the tracing project page, then click on New Evaluator.2. Name your evaluator
3. Create a filter
For example, you may want to apply specific evaluators based on:- Runs where a user left feedback indicating the response was unsatisfactory.
- Runs that invoke a specific tool call. See filtering for tool calls for more information.
- Runs that match a particular piece of metadata (e.g. if you log traces with a
plan_type
and only want to run evaluations on traces from your enterprise customers). See adding metadata to your traces for more information.
It’s often helpful to inspect runs as you’re creating a filter for your evaluator. With the evaluator configuration panel open, you can inspect runs and apply filters to them. Any filters you apply to the runs table will automatically be reflected in filters on your evaluator.
4. (Optional) Configure a sampling rate
Configure a sampling rate to control the percentage of filtered runs that trigger the automation action. For example, to control costs, you may want to set a filter to only apply the evaluator to 10% of traces. In order to do this, you would set the sampling rate to 0.1.5. (Optional) Apply rule to past runs
Apply rule to past runs by toggling the Apply to past runs and entering a “Backfill from” date. This is only possible upon rule creation. Note: the backfill is processed as a background job, so you will not see the results immediately. In order to track progress of the backfill, you can view logs for your evaluator by heading to the Evaluators tab within a tracing project and clicking the Logs button for the evaluator you created. Online evaluator logs are similar to automation rule logs.- Add an evaluator name
- Optionally filter runs that you would like to apply your evaluator on or configure a sampling rate.
- Select Apply Evaluator
6. Select evaluator type
- Configuring LLM-as-a-judge evaluators
- Configuring custom code evaluators
Configure a LLM-as-a-judge online evaluator
View this guide to configure an LLM-as-a-judge evaluator.Configure a custom code evaluator
Select custom code evaluator.Write your evaluation function
Custom code evaluators restrictions.Allowed Libraries: You can import all standard library functions, as well as the following public packages:Network Access: You cannot access the internet from a custom code evaluator.
- A
Run
(reference). This represents the sampled run to evaluate.
- Feedback(s) Dictionary: A dictionary whose keys are the type of feedback you want to return, and values are the score you will give for that feedback key. For example,
{"correctness": 1, "silliness": 0}
would create two types of feedback on the run, one saying it is correct, and the other saying it is not silly.