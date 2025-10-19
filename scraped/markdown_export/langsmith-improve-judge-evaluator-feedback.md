# langsmith-improve-judge-evaluator-feedback

> Source: https://docs.langchain.com/langsmith/improve-judge-evaluator-feedback

Reliable LLM-as-a-judge evaluators are critical for making informed decisions about your AI applications (e.g., prompt, model, architecture changes). Defining the evaluator prompt correctly can be difficult, but it directly affects the trustworthiness of your evaluations.
This guide describes how to align your LLM-as-a-judge evaluator using human feedback to improve your evaluator’s quality and help you build reliable AI applications.
How it works
LangSmith’s Align Evaluator feature has a series of steps that help you align your LLM-as-a-judge evaluator with human expert feedback. You can use this feature to align evaluators that run on a dataset for offline evaluations or for online evaluations. In either case, the steps are similar:- Select experiments or runs that contain outputs from your application.
- Add the selected experiments or runs to an annotation queue where a human expert can label the data.
- Test your LLM-as-a-judge evaluator prompt against the labeled examples. Check the cases where your evaluator result is not aligned with the labeled data. This indicates areas where your evaluator prompt needs improvement.
- Refine and repeat to improve evaluator alignment. Update your LLM-as-a-judge evaluator prompt and test again.
Prerequisites
You’ll need the following before starting this guide for offline evaluations or online evaluations:Offline evaluations
- A dataset with at least one experiment.
- You’ll need to upload or create datasets via the SDK or the UI and run an experiment via the SDK or the Playground.
Online evaluations
- An application that’s already sending traces to LangSmith.
- Configure this with one of the tracing integrations to start.
Getting started
You can enter the alignment flow for both new and existing evaluators in datasets and tracing projects.| Dataset Evaluators | Tracing Project Evaluators | |
|---|---|---|
| Create an aligned evaluator from scratch | 1. Datasets & Experiments and select your dataset 2. Click + Evaluator > Create from labeled data 3. Enter a descriptive feedback key name (e.g. correctness , hallucination ) | 1. Projects and select your project 2. Click + New > Evaluator > Create from labeled data 3. Enter a descriptive feedback‑key name (e.g. correctness , hallucination ) |
| Align an existing evaluator | 1. Datasets & Experiments > select your dataset > Evaluators tab 2. In the Align Evaluator with experiment data box, click Select Experiments | 1. Projects > select your project > Evaluators tab 2. In the Align Evaluator with experiment data box, click Select Experiments |
1. Select experiments or runs
Select one or more experiments (or runs) to send for human labeling. This will add runs to an annotation queue. To add any new experiments/runs to an existing annotation queue, head to the Evaluators tab, select the evaluator you are aligning and click Add to Queue.Datasets should be representative of inputs and outputs you expect to see in production.While you don’t need to cover every possible scenario, it’s important to include examples across the full range of expected use cases. For example, if you’re building a sports bot that answers questions about baseball, basketball, and football, your dataset should include at least one labeled example from each sport.
2. Label examples
Label examples in the annotation queue by adding a feedback score. Once you’ve labeled an example, click Add to Reference Dataset.If you have a large number of examples in your experiments, you don’t need to label every example to get started. We recommend starting with at least 20 examples, you can always add more later. We recommend that the examples that you label are diverse (balanced in both 0 and 1 labels) to ensure that you’re building a well rounded evaluator prompt.
3. Test your evaluator prompt against the labeled examples
Once you have labeled examples, the next step is iterating on your evaluator prompt to mimic the labeled data as well as possible. This iteration is done in the Evaluator Playground. To go to the evaluator playground: Click the View evaluator button on the top right of the evaluator queue. This will take you to the detail page of the evaluator you are aligning. Click the Evaluator Playground button to access the playground. In the evaluator playground you can create or edit your evaluator prompt and click Start Alignment to run it over the set of labeled examples that you created in Step 2. After running your evaluator, you’ll see how its generated scores compare to your human labels. The alignment score is the percentage of examples where the evaluator’s judgment matches that of the human expert.4. Repeat to improve evaluator alignment
Iterate by updating your prompt and testing again to improve evaluator alignment.Updates to your evaluator prompt are not saved by default. We reccomend saving your evaluator prompt regularly, and especially after you see your alignment score improve.The evaluator playground will show the alignment score for the most recently saved version of your evaluator prompt for comparison when you’re iterating on your prompt.