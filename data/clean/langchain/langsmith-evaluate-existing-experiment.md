---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-evaluate-existing-experiment",
  "h1": "langsmith-evaluate-existing-experiment",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.486555",
  "sha256_raw": "d27368530e0f26f76345e36711a0f2de1a983ba784fffb49a89670c6db4a0b82"
}
---

# langsmith-evaluate-existing-experiment

> Source: https://docs.langchain.com/langsmith/evaluate-existing-experiment

How to evaluate an existing experiment (Python only)
Evaluation of existing experiments is currently only supported in the Python SDK.If you have already run an experiment and want to add additional evaluation metrics, you can apply any evaluators to the experiment using the evaluate() / aevaluate() methods as before. Just pass in the experiment name / ID instead of a target function:
Copy
from langsmith import evaluatedef always_half(inputs: dict, outputs: dict) -> float: return 0.5experiment_name = "my-experiment:abc" # Replace with an actual experiment name or IDevaluate(experiment_name, evaluators=[always_half])