---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-fetch-perf-metrics-experiment",
  "h1": "langsmith-fetch-perf-metrics-experiment",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.487058",
  "sha256_raw": "540edf3c32cafdee2d0d1ed1916f99670a17a7b831bcace73ebdfb4641983f97"
}
---

# langsmith-fetch-perf-metrics-experiment

> Source: https://docs.langchain.com/langsmith/fetch-perf-metrics-experiment

Tracing projects and experiments use the same underlying data structure in our backend, which is called a “session.”You might see these terms interchangeably in our documentation, but they all refer to the same underlying data structure.We are working on unifying the terminology across our documentation and APIs.
evaluate
with the Python or TypeScript SDK, you can fetch the performance metrics for the experiment using the read_project
/readProject
methods.
The payload for experiment details includes the following values:
latency_p50
: The 50th percentile latency in seconds.latency_p99
: The 99th percentile latency in seconds.total_tokens
: The total number of tokens used.prompt_tokens
: The number of prompt tokens used.completion_tokens
: The number of completion tokens used.total_cost
: The total cost of the experiment.prompt_cost
: The cost of the prompt tokens.completion_cost
: The cost of the completion tokens.feedback_stats
: The feedback statistics for the experiment.error_rate
: The error rate for the experiment.first_token_p50
: The 50th percentile latency for the time to generate the first token (if using streaming).first_token_p99
: The 99th percentile latency for the time to generate the first token (if using streaming).
evaluate
, then fetch the performance metrics for the experiment.