---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-repetition",
  "h1": "langsmith-repetition",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.436309",
  "sha256_raw": "fbcb6c10ed66f83e967dac13b4740ed5a139c8b13872195427d5627c8bba76ea"
}
---

# langsmith-repetition

> Source: https://docs.langchain.com/langsmith/repetition

Running multiple repetitions can give a more accurate estimate of the performance of your system since LLM outputs are not deterministic. Outputs can differ from one repetition to the next. Repetitions are a way to reduce noise in systems prone to high variability, such as agents.
Add the optional num_repetitions param to the evaluate / aevaluate function (Python, TypeScript) to specify how many times to evaluate over each example in your dataset. For instance, if you have 5 examples in the dataset and set num_repetitions=5, each example will be run 5 times, for a total of 25 runs.
Viewing results of experiments run with repetitions
If you’ve run your experiment with repetitions, there will be arrows in the output results column so you can view outputs in the table. To view each run from the repetition, hover over the output cell and click the expanded view. When you run an experiment with repetitions, LangSmith displays the average for each feedback score in the table. Click on the feedback score to view the feedback scores from individual runs, or to view the standard deviation across repetitions.