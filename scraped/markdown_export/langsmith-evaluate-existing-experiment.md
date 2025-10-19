# langsmith-evaluate-existing-experiment

> Source: https://docs.langchain.com/langsmith/evaluate-existing-experiment

How to evaluate an existing experiment (Python only)
Evaluation of existing experiments is currently only supported in the Python SDK.If you have already run an experiment and want to add additional evaluation metrics, you can apply any evaluators to the experiment using the evaluate() / aevaluate() methods as before. Just pass in the experiment name / ID instead of a target function:
Copy
from langsmith import evaluatedef always_half(inputs: dict, outputs: dict) -> float: return 0.5experiment_name = "my-experiment:abc" # Replace with an actual experiment name or IDevaluate(experiment_name, evaluators=[always_half])