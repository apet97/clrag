---
{
  "url": "",
  "namespace": "langchain",
  "title": "langsmith-evaluation-async",
  "h1": "langsmith-evaluation-async",
  "h2": [],
  "fetched_at": "2025-10-19T19:18:02.484435",
  "sha256_raw": "ec6e8c814f0e2b5460efb828b491b3d4be66849eea8aaf8adb3d43a6fb13bef8"
}
---

# langsmith-evaluation-async

> Source: https://docs.langchain.com/langsmith/evaluation-async

We can run evaluations asynchronously via the SDK using aevaluate(), which accepts all of the same arguments as evaluate() but expects the application function to be asynchronous. You can learn more about how to use the evaluate() function here.
This guide is only relevant when using the Python SDK. In JS/TS the evaluate() function is already async. You can see how to use it here.
from langsmith import wrappers, Clientfrom openai import AsyncOpenAI# Optionally wrap the OpenAI client to trace all model calls.oai_client = wrappers.wrap_openai(AsyncOpenAI())# Optionally add the 'traceable' decorator to trace the inputs/outputs of this function.@traceableasync def researcher_app(inputs: dict) -> str: instructions = """You are an excellent researcher. Given a high-level research idea, \list 5 concrete questions that should be investigated to determine if the idea is worth pursuing.""" response = await oai_client.chat.completions.create( model="gpt-4o-mini", messages=[ {"role": "system", "content": instructions}, {"role": "user", "content": inputs["idea"]}, ], ) return response.choices[0].message.content# Evaluator functions can be sync or asyncdef concise(inputs: dict, outputs: dict) -> bool: return len(outputs["output"]) < 3 * len(inputs["idea"])ls_client = Client()ideas = [ "universal basic income", "nuclear fusion", "hyperloop", "nuclear powered rockets",]dataset = ls_client.create_dataset("research ideas")ls_client.create_examples( dataset_name=dataset.name, examples=[{"inputs": {"idea": i}} for i in ideas],)# Can equivalently use the 'aevaluate' function directly:# from langsmith import aevaluate# await aevaluate(...)results = await ls_client.aevaluate( researcher_app, data=dataset, evaluators=[concise], # Optional, add concurrency. max_concurrency=2, # Optional, add concurrency. experiment_prefix="gpt-4o-mini-baseline" # Optional, random by default.)