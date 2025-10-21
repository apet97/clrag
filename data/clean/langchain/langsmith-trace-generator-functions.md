---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-trace-generator-functions",
  "h1": "langsmith-trace-generator-functions",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.469357",
  "sha256_raw": "bb9da9ee7adc1422c19d671a3ee709737ddb45779815fb4f185ff6018ad1fa8a"
}
---

# langsmith-trace-generator-functions

> Source: https://docs.langchain.com/langsmith/trace-generator-functions

generator
functions. Below is an example.
outputs
of the traced function are aggregated into a single array in LangSmith. If you want to customize how it is stored (for instance, concatenating the outputs into a single string), you can use the aggregate
option (reduce_fn
in python). This is especially useful for aggregating streamed LLM outputs.
Aggregating outputs only impacts the traced representation of the outputs. It doesn not alter the values returned by your function.